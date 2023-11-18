import typing as ty
import argparse
import logging
from pydantic import BaseModel
from markdown_it import MarkdownIt
from markdown_it.token import Token
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def unescape_code_blocks(content: str) -> str:
    """
    Unescapes escaped code blocks within Markdown content.

    This function is used to handle the special case where code blocks within
    Markdown files have been escaped to prevent conflicts with the Markdown syntax.

    Args:
        content (str): The Markdown content with potentially escaped code blocks.

    Returns:
        str: The Markdown content with code blocks unescaped.
    """
    return content.replace("<!--SLOPIFY_CODE_BLOCK```-->", "```")


# def apply_markdown(markdown_content: str, base_path: ty.Optional[Path] = None):
#     """
#     Writes a set of files serialised as slopify markdown back to the file system.

#     For every type of included file except markdown files, this just writes the code 
#     blocks, which by construction represent the file content.

#     For markdown files themselves (for example, README.md, CONTRIBUTING.md) which 
#     are serialised inside slopify markdown, we have to deal with the case where 
#     markdown content (represented by a markdown code block) must be written back 
#     to a markdown file. This markdown code block may itself include
#     code blocks which have been escaped by slopify upon serialisation. The full 
#     contents of this markdown code block must be written back to a markdown file 
#     with the code blocks unescaped.
#     """
#     md = MarkdownIt()
#     tokens = md.parse(markdown_content)

class FileContent(BaseModel):
    """
    A simple data structure to hold the path and content for a file.

    Attributes:
        path (Path): The path where the file should be written.
        content (str): The content to be written to the file.
    """
    path: Path
    content: str

def parse_markdown(tokens: list[Token], base_path: Path) -> list[FileContent]:
    """
    Parses a list of Markdown tokens and extracts the file paths and contents.

    The markdown tokens are presumed to come from a slopify markdown dump, 
    i.e. markdown used to serialise file contents in a specific way.

    This function assumes that each file's content is represented as a code block
    immediately following an H1 heading with the file's relative path. 
    For Markdown files, all content between file headers is included. It also
    handles the special case of Markdown files that may contain nested code blocks,
    which need to be unescaped before writing back to the file system.

    Args:
        tokens (list[Token]): A list of tokens obtained from parsing Markdown content.
        base_path (Path): The base path relative to which file paths will be resolved.

    Returns:
        list[FileContent]: A list of FileContent objects with extracted paths and contents.
    """
    file_contents = []
    current_path = None
    current_content_lines = []
    capture_markdown_content = False  # Flag to capture all content for Markdown files

    for token in tokens:
        if token.type == 'heading_open' and token.tag == 'h1' and not capture_markdown_content:
            # If we already have a path and content, save them before starting a new file
            if current_path is not None:
                content = '\n'.join(current_content_lines)
                file_contents.append(FileContent(path=current_path, content=content))
            current_path = None
            current_content_lines = []
            capture_markdown_content = False  # Reset the flag
        elif token.type == 'inline' and current_path is None:
            # Extract the file path from the inline token's content
            current_path = base_path / token.content.strip('`')
            # Check if the current file is a Markdown file
            capture_markdown_content = current_path.suffix == '.md'
        elif capture_markdown_content:
            # Capture all content for Markdown files
            if token.type == 'fence':
                # For code blocks, capture the content including the backticks and language info
                current_content_lines.append(unescape_code_blocks(token.content))#f"```{token.info}\n{token.content}```")
            elif token.type == 'heading_open':
                # preserve heading level based on tag
                heading_level = token.tag.lstrip("h")
                current_content_lines.append(f"{'#' * int(heading_level)}")
                continue
            else:
                # For non-code block content, capture the raw content
                current_content_lines.append(token.content)
        elif token.type == 'fence' and current_path is not None and not capture_markdown_content:
            # For non-Markdown files, capture only the code block content
            current_content_lines.append(token.content)

    # Handle the last file content if any
    if current_path is not None:
        content = '\n'.join(current_content_lines)
        file_contents.append(FileContent(path=current_path, content=content))

    return file_contents

def write_files(file_contents: list[FileContent]):
    """
    Writes the content of each FileContent object to the filesystem.

    This function is responsible for creating any necessary directories and writing
    the file content to the specified paths. It also handles the special case of
    Markdown files, ensuring that any nested code blocks are correctly unescaped
    before writing.

    Args:
        file_contents (list[FileContent]): A list of FileContent objects to be written.
    """
    for file_content in file_contents:
        file_path = file_content.path
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Create directories if needed
        with file_path.open('w', encoding='utf-8') as file:
            file.write(file_content.content)


def apply_markdown(markdown_content: str, base_path: ty.Optional[Path] = None):
    """
    Applies Markdown content to the filesystem, writing files as described in the content.

    This function parses the Markdown content, extracts file paths and contents,
    unescapes code blocks if necessary, and writes the content to the filesystem.
    It handles the special case of Markdown files that may contain nested code blocks,
    ensuring that they are correctly unescaped before writing.

    Args:
        markdown_content (str): The Markdown content to be applied.
        base_path (Path, optional): The base directory for applying the code. Defaults to the current working directory.
    """
    md = MarkdownIt()
    tokens = md.parse(markdown_content)

    # Step 2: Refine the Parsing Logic
    base_path = base_path or Path.cwd()
    file_contents = parse_markdown(tokens, base_path)
    logger.debug(f"{file_contents=}")
    # Step 4: Handle Special Cases
    for file_content in file_contents:
        if file_content.path.suffix == '.md':
            file_content.content = unescape_code_blocks(file_content.content)
    logger.debug(f"{file_contents=}")
    # Step 3: Verify File Writing Logic
    write_files(file_contents)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Markdown file to directory.")
    parser.add_argument(
        "markdown_file", type=str, help="Path to the Markdown file to apply."
    )
    args = parser.parse_args()
    apply_markdown(args.markdown_file)
