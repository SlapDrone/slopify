import typing as ty
import argparse
from markdown_it import MarkdownIt
from pathlib import Path


def unescape_code_blocks(content: str) -> str:
    """
    Unescape code blocks by removing the unique HTML comments.
    """
    return content.replace("<!--SLOPIFY_CODE_BLOCK```-->", "```")


def apply_markdown(markdown_file: Path, base_path: ty.Optional[Path] = None):
    md = MarkdownIt()
    tokens = md.parse(markdown_file.read_text(encoding="utf-8"))

    code_blocks = {}
    current_file_path = None

    for token in tokens:
        if token.type == "heading_open" and token.tag == "h1":
            # The next token is the text of the heading, which contains the file path
            current_file_path = tokens[tokens.index(token) + 1].content.strip("`")
        elif token.type == "fence" and current_file_path:
            # This token contains the content of the code block
            code_blocks[current_file_path] = token.content

    # Apply the code blocks to the file system
    for file_path, code in code_blocks.items():
        if file_path.endswith(".md"):
            # Unescape code blocks within Markdown files
            code = unescape_code_blocks(code)
        full_path = (base_path or markdown_file.parent) / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with full_path.open("w", encoding="utf-8") as f:
            f.write(code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Markdown file to directory.")
    parser.add_argument(
        "markdown_file", type=str, help="Path to the Markdown file to apply."
    )
    args = parser.parse_args()
    apply_markdown(args.markdown_file)
