#!/usr/bin/env uv run

import ast
import glob
import os
import sys
import textwrap
from pathlib import Path
from typing import Iterator, Literal, cast

import marko
import requests
from marko.block import FencedCode
from marko.element import Element
from marko.inline import RawText

GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_SHA = os.environ["GITHUB_SHA"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


def create_check(
    in_progress=False,
    conclusion=None,
    summary="",
    text="",
):
    payload = {
        "name": "Code Block Check",
        "head_sha": GITHUB_SHA,
        "status": "in_progress" if in_progress else "completed",
    }

    if not in_progress:
        payload.update(
            {
                # one of: success, failure, neutral, cancelled, timed_out, action_required
                "conclusion": conclusion,
                "output": {
                    "title": "Code Block Check",
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
    else:
        print("✅ GitHub Check created successfully")


def text_from_code_block(code_block: FencedCode) -> str:
    if len(code_block.children) != 1:
        raise ValueError("unexpected number of children for FencedCode")

    raw_text: RawText = cast(RawText, code_block.children[0])

    return raw_text.children


def find_fenced_code(ast_node: Element) -> Iterator[FencedCode]:
    """Recursively yield all FencedCode blocks in the AST."""
    if isinstance(ast_node, FencedCode):
        yield ast_node
    elif hasattr(ast_node, "children"):
        for child in ast_node.children:
            yield from find_fenced_code(child)


def extract_code_blocks(
    markdown: str,
) -> list[tuple[Literal["PYTHON"] | Literal["MISSING"], str]]:
    """Extract python code blocks from markdown"""
    markdown_ast = marko.parse(markdown)

    code_blocks: list[tuple[Literal["PYTHON"] | Literal["MISSING"], str]] = []

    for code_block in find_fenced_code(markdown_ast):
        if not code_block.lang:
            code_blocks.append(("MISSING", text_from_code_block(code_block)))
        elif code_block.lang.lower() == "python":
            code_blocks.append(("PYTHON", text_from_code_block(code_block)))
        else:
            # we could also parse JSON, XML, etc. if desired
            pass

    return code_blocks


def extract_doctest_blocks(text):
    blocks = []
    current = []

    for line in text.splitlines():
        if line.startswith(">>>"):
            current.append(line[4:])
        elif line.startswith("...") and current:
            current.append(line[4:])
        else:
            if current:
                blocks.append("\n".join(current))
                current = []

    if current:
        blocks.append("\n".join(current))

    return blocks


def run_code_snippet(snippet, file_path, index):
    if ">>>" in snippet:
        new_blocks = extract_doctest_blocks(snippet)
        results = []

        for block in new_blocks:
            results.append(run_code_snippet(block, file_path, index))

        return all(result for result in results)

    try:
        parsed = ast.parse(
            textwrap.dedent(snippet),
            filename=f"{file_path} block #{index}",
        )

        compile(parsed, filename=f"{file_path} block #{index}", mode="exec")

        import_nodes = [
            node
            for node in parsed.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        import_src = "\n".join(textwrap.dedent(ast.unparse(n)) for n in import_nodes)

        exec(import_src, {})

        print(f"✅ Syntax OK {file_path} block #{index}")

        return True
    except ModuleNotFoundError as e:
        print(f"❌ Missing import: {e}")
        return False
    except SyntaxError as e:
        print(f"❌ SyntaxError in {file_path} block #{index}: {e}")
        return False
    except Exception as e:
        print(f"❌ Other parse error in {file_path} block #{index}: {e}")
        return False


def print_code_block(code_block: str) -> None:
    print()
    print(
        "\n".join(
            f"{i + 1: <5} {line}" for i, line in enumerate(code_block.splitlines())
        )
    )
    print()


def main():
    create_check(in_progress=True)

    failures = 0
    total_code_blocks = 0
    missing_language = 0

    for markdown_file in glob.iglob("**/*.md", recursive=True):
        if "node_modules" in markdown_file:
            continue

        content = Path(markdown_file).read_text()
        code_blocks = extract_code_blocks(content)

        for index, (language, block) in enumerate(code_blocks):
            if language == "PYTHON":
                total_code_blocks += 1

                if not run_code_snippet(block, markdown_file, index + 1):
                    print_code_block(block)

                    failures += 1
            elif language == "MISSING":
                missing_language += 1

                print(f"❌ Missing language in {markdown_file} block #{index + 1}")
                print_code_block(block)

    print()
    print(f"ℹ️ {total_code_blocks} Python code blocks found")

    if failures or missing_language:
        create_check(conclusion="failure", summary="", text="")

        print(f"💻 {missing_language} code blocks missing language")
        print(f"💥 {failures} code blocks failed")

        sys.exit(1)
    else:
        create_check(conclusion="success", summary="", text="")

        print("🎉 all code blocks passed!")


if __name__ == "__main__":
    main()
