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


def find_missing_imports(snippet: str, filename: str) -> set[str]:
    src = textwrap.dedent(snippet)
    top = symtable.symtable(src, filename, "exec")

    missing = set()

    for sym in top.get_symbols():
        name = sym.get_name()

        if name in BUILTINS:
            continue

        if sym.is_referenced() and not (
            sym.is_imported() or sym.is_assigned() or sym.is_parameter() or sym.is_namespace()
        ):
            missing.add(name)

    return missing


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
