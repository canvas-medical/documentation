#!/usr/bin/env uv run

import ast
import glob
import re
import sys
import textwrap
from pathlib import Path

ROOT_DIR = Path(__file__).resolve()
MARKDOWN_DIR = ROOT_DIR  # or wherever your .md files live


def extract_code_blocks(md_content):
    """Extract ```python code blocks from markdown"""
    pattern = r"```(?:python\n)(.*?)```"
    return re.findall(pattern, md_content, flags=re.DOTALL | re.MULTILINE)


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
        parsed = ast.parse(snippet, filename=f"{file_path} block #{index}")

        compile(parsed, filename=f"{file_path} block #{index}", mode="exec")

        import_nodes = [
            node
            for node in parsed.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        import_src = "\n".join(textwrap.dedent(ast.unparse(n)) for n in import_nodes)

        exec(import_src, {})

        print(f"✅ Syntax OK {file_path}, block #{index}")

        return True
    except ModuleNotFoundError as e:
        print(f"❌ Missing import: {e}")
        return False
    except SyntaxError as e:
        print(f"\n❌ SyntaxError in {file_path}, block #{index}: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Other parse error in {file_path}, block #{index}: {e}")
        return False


def main():
    failures = 0
    md_files = glob.glob("**/*.md", recursive=True)

    for md_file in md_files:
        if "node_modules" in md_file:
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        blocks = extract_code_blocks(content)

        for idx, block in enumerate(blocks):
            if not run_code_snippet(block, md_file, idx + 1):
                print()
                print(
                    "\n".join(
                        f"{i: <5} {line}" for i, line in enumerate(block.splitlines())
                    )
                )
                print()

                failures += 1

    if failures:
        print(f"\n💥 {failures} code blocks failed.")

        sys.exit(1)
    else:
        print("\n🎉 all code blocks passed.")


if __name__ == "__main__":
    main()
