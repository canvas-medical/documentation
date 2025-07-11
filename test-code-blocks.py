#!/usr/bin/env uv run

import ast
import glob
from pathlib import Path
import sys
import marko
import textwrap
from typing import Iterator, Literal, cast
from marko.block import FencedCode
from marko.element import Element
from marko.inline import RawText


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
        print(f"💻 {missing_language} code blocks missing language")
        print(f"💥 {failures} code blocks failed")

        sys.exit(1)
    else:
        print("🎉 all code blocks passed!")


if __name__ == "__main__":
    main()
