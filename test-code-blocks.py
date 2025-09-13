#!/usr/bin/env uv run

from __future__ import annotations

import ast
import builtins
import glob
import os
import symtable
import sys
import textwrap
from pathlib import Path
from typing import Any, Literal, cast

import click
import requests
from markdown_it import MarkdownIt

Kind = Literal["PYTHON"] | Literal["PYTHON_IMPORTS_ONLY"] | Literal["MISSING"]


GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_SHA = os.environ.get("GITHUB_SHA")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_PYTHON_VERSION = os.environ.get("GITHUB_PYTHON_VERSION")

BUILTINS = set(dir(builtins))


def create_check(
    in_progress: bool = False,
    conclusion: str | None = None,
    summary: str = "",
    text: str = "",
) -> None:
    if not GITHUB_REPOSITORY:
        return

    title = f"Code Block Check: {GITHUB_PYTHON_VERSION}"

    payload: dict[str, Any] = {
        "name": title,
        "head_sha": GITHUB_SHA,
        "status": "in_progress" if in_progress else "completed",
    }

    if not in_progress:
        payload.update(
            {
                # one of: success, failure, neutral, cancelled, timed_out, action_required
                "conclusion": conclusion,
                "output": {
                    "title": title,
                    "summary": summary,
                    "text": text,
                },
            }
        )

    response = requests.post(
        f"https://api.github.com/repos/{GITHUB_REPOSITORY}/check-runs",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        json=payload,
    )

    if response.status_code >= 300:
        print(f"❌ Failed to create check: {response.status_code}")
        print(response.text)


def extract_code_blocks(
    markdown: str,
) -> list[tuple[Kind, str, tuple[int, int]]]:
    """
    Return (kind, code, (start_line, end_line))
    note: start/end are line numbers from markdown-it-py token.map.
          they’re 0-based in upstream; treat as half-open [start, end).
    """
    md = MarkdownIt("commonmark")
    tokens = md.parse(markdown)

    code_blocks: list[tuple[Kind, str, tuple[int, int]]] = []

    for tok in tokens:
        if tok.type != "fence":
            continue

        info = (tok.info or "").strip().lower()
        lang = info.split()[0] if info else ""

        kind: Kind | None = None

        if not lang:
            kind = "MISSING"
        elif lang.lower() == "python":
            kind = "PYTHON"
        elif lang.lower() == "python?partial=true":
            kind = "PYTHON_IMPORTS_ONLY"

        if kind:
            code_blocks.append(
                (
                    kind,
                    tok.content,
                    cast(tuple[int, int] | None, tok.map) or (-1, -1),
                )
            )

    return code_blocks


def extract_doctest_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []

    for line in text.splitlines():
        if line.startswith(">>>") or line.startswith("...") and current:
            current.append(line[4:])
        else:
            if current:
                blocks.append("\n".join(current))
                current = []

    if current:
        blocks.append("\n".join(current))

    return blocks


def _walk_tables(t: symtable.SymbolTable) -> Any:
    yield t

    for c in t.get_children():
        yield from _walk_tables(c)


def _missing_via_symtable(src: str, filename: str) -> set[str]:
    """Real refs that aren't imported/assigned/params in their scope."""
    top = symtable.symtable(src, filename, "exec")
    missing: set[str] = set()

    def rec(tbl: symtable.SymbolTable, inherited: set[str]) -> None:
        local_defined = {
            s.get_name()
            for s in tbl.get_symbols()
            if s.is_imported() or s.is_parameter() or s.is_assigned() or s.is_namespace()
        }

        visible = inherited | local_defined | BUILTINS

        for s in tbl.get_symbols():
            n = s.get_name()

            if s.is_referenced() and n not in visible:
                missing.add(n)

        for child in tbl.get_children():
            rec(child, visible)

    rec(top, set())

    return missing


class _AnnOnly(ast.NodeVisitor):
    """collect names that appear *only* in annotations (skip bodies)."""

    def __init__(self) -> None:
        self.names: set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        self.names.add(node.id)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        self.visit(node.value)
        # py3.9+: slice is an expr
        if hasattr(node, "slice") and isinstance(node.slice, ast.AST):
            self.visit(node.slice)

    def _anno(self, a: Any) -> None:
        if not a:
            return

        # handle stringified annotations
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            try:
                a = ast.parse(a.value, mode="eval").body
            except Exception:
                return

        self.visit(a)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for a in node.args.args + node.args.kwonlyargs:
            self._anno(a.annotation)
        if node.args.vararg:
            self._anno(node.args.vararg.annotation)
        if node.args.kwarg:
            self._anno(node.args.kwarg.annotation)

        self._anno(node.returns)
        # do NOT generic_visit: we intentionally skip the body

    visit_AsyncFunctionDef = visit_FunctionDef  # type: ignore[assignment]

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self._anno(node.annotation)
        # skip value


def find_missing_imports(snippet: str, filename: str = "<doc>") -> set[str]:
    src = textwrap.dedent(snippet)

    # 1) true free names via symtable (handles class bodies, params, scopes)
    miss = _missing_via_symtable(src, filename)

    # 2) names used only in annotations
    tree = ast.parse(src, filename=filename, mode="exec")
    ann = _AnnOnly()
    ann.visit(tree)

    # union of all defined names across all scopes
    top = symtable.symtable(src, filename, "exec")
    defined: set[str] = set()
    for tbl in _walk_tables(top):
        for s in tbl.get_symbols():
            if s.is_imported() or s.is_parameter() or s.is_assigned() or s.is_namespace():
                defined.add(s.get_name())

    ann_miss = {n for n in ann.names if n not in defined and n not in BUILTINS}

    return (miss | ann_miss) - BUILTINS


def check_code(
    snippet: str,
    file_path: str,
    position: tuple[int, int],
    imports_only: bool = False,
) -> tuple[bool, str]:
    block_name = f"{file_path}:{position[0]}"

    if ">>>" in snippet:
        new_blocks = extract_doctest_blocks(snippet)
        results = []

        for block in new_blocks:
            results.append(check_code(block, file_path, position))

        if all(result for result, _ in results):
            return True, f"✅ {block_name}"
        else:
            return False, "\n".join(message for _, message in results)

    if not imports_only:
        try:
            parsed = ast.parse(
                textwrap.dedent(snippet),
                filename=block_name,
            )

            compile(parsed, filename=block_name, mode="exec")

            import_nodes = [
                node for node in parsed.body if isinstance(node, (ast.Import, ast.ImportFrom))
            ]

            import_src = "\n".join(textwrap.dedent(ast.unparse(n)) for n in import_nodes)

            exec(import_src, {})
        except SyntaxError as e:
            return False, f"❌ SyntaxError in {block_name}: {e}"
        except ModuleNotFoundError as e:
            return False, f"❌ Missing import in {block_name}: {e}"
        except Exception as e:
            return False, f"❌ Other parse error in {block_name}: {e}"

        missing_imports = find_missing_imports(snippet, block_name)

        if missing_imports:
            return False, f"❌ Missing import(s) {block_name}: {', '.join(missing_imports)}"

    return True, f"✅ {block_name}"


def code_block_text(code_block: str) -> str:
    return (
        "\n"
        + "\n".join(f"{i + 1: <5} {line}" for i, line in enumerate(code_block.splitlines()))
        + "\n"
    )


@click.command()
@click.option("-f", "--fail-fast", default=False, help="exit on the first failure", is_flag=True)
@click.option("-q", "--quiet", default=False, help="only log failures", is_flag=True)
def check(fail_fast: bool = False, quiet: bool = False) -> None:
    create_check(in_progress=True)

    failures = 0
    total_code_blocks = 0
    missing_language = 0

    text_output = ""

    for markdown_file in glob.iglob("**/*.md", recursive=True):
        if "node_modules" in markdown_file:
            continue

        # Choosing to skip generated example plugin documentation.
        # These docs include whole files directly from the plugin, which may
        # reference other files within that plugin package. Those imports will
        # not resolve.
        if "collections/_sdk/examples/" in markdown_file:
            continue

        content = Path(markdown_file).read_text()
        code_blocks = extract_code_blocks(content)

        for language, block, position in code_blocks:
            if language in ("PYTHON", "PYTHON_IMPORTS_ONLY"):
                total_code_blocks += 1

                success, message = check_code(
                    block,
                    markdown_file,
                    position,
                    imports_only=language == "PYTHON_IMPORTS_ONLY",
                )

                if success:
                    if not quiet:
                        print(message)
                else:
                    text = message + "\n" + code_block_text(block)
                    text_output += text

                    failures += 1

                    print(text)

                    if fail_fast:
                        sys.exit(1)
            elif language == "MISSING":
                missing_language += 1

                text = f"❌ Missing language in {markdown_file}:{position[0]}\n"
                text += code_block_text(block)

                text_output += text

                print(text)

                if fail_fast:
                    sys.exit(1)

    summary = f"ℹ️ {total_code_blocks} Python code blocks found\n"

    if failures or missing_language:
        summary += f"💻 {missing_language} code blocks missing language\n"
        summary += f"💥 {failures} code blocks failed"

        create_check(conclusion="failure", summary=summary, text=text_output)
    else:
        summary += "🎉 all code blocks passed!"

        create_check(conclusion="success", summary=summary)

    print(summary)

    if failures or missing_language:
        sys.exit(1)


if __name__ == "__main__":
    check()
