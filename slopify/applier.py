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


class FileContent(BaseModel):
    """
    A data structure to hold the path and content for a file, along with any extra content.

    Attributes:
        path (Path): The path where the file should be written.
        content (str): The main content to be written to the file.
        extra_content (str): Any additional content that is not part of the main content.
    """
    path: Path
    content: str
    extra_content: str = ""  # Additional attribute for extra content


def parse_markdown_headings(markdown_text: str) -> dict[str, str]:
    """
    Parses a Markdown string and extracts content under each H1 heading.

    Args:
        markdown_text (str): The Markdown text to be parsed.

    Returns:
        Dict[str, str]: A dictionary where each key is an H1 heading and 
                        the value is the content under that heading.
    """
    md = MarkdownIt()
    tokens = md.parse(markdown_text)
    lines = markdown_text.split('\n')

    headings = {}
    current_heading = None
    current_heading_line = -1

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == 'heading_open' and token.tag == 'h1':
            if current_heading is not None:
                content_lines = lines[current_heading_line + 1:token.map[0]]
                headings[current_heading] = '\n'.join(content_lines).strip()

            current_heading_line = token.map[0]
            i += 1  # Move to the next token

            while i < len(tokens) and tokens[i].type != 'inline':
                i += 1

            if i < len(tokens):
                current_heading = tokens[i].content
                i += 1  # Skip past the inline token

        else:
            i += 1  # Move to the next token

    if current_heading is not None:
        content_lines = lines[current_heading_line + 1:]
        headings[current_heading] = '\n'.join(content_lines).strip()

    return headings
    

def create_file_contents_from_markdown(markdown_text: str, base_path: str) -> list[FileContent]:
    """
    Creates FileContent objects from a Markdown string where each H1 heading denotes a file path.

    Args:
        markdown_text (str): The Markdown text representing serialized files.
        base_path (str): The base path to be prefixed to each file path.

    Returns:
        List[FileContent]: A list of FileContent objects representing the files.
    """
    parsed_headings = parse_markdown_headings(markdown_text)
    file_contents = []

    for heading, content in parsed_headings.items():
        file_path = heading.strip('`')
        full_path = Path(base_path) / file_path
        file_content = FileContent(path=full_path, content=content)
        file_contents.append(file_content)

    return file_contents

def postprocess_content(file_content: FileContent) -> FileContent:
    """
    Post-processes the content of a FileContent object based on its file type.

    For Markdown files (.md), it unescapes commented-out code blocks and removes the enclosing code block syntax.
    For non-Markdown files, it extracts only the content of the single code block, handling the potential presence of a language identifier.

    Args:
        file_content (FileContent): The FileContent object to be post-processed.

    Returns:
        FileContent: The post-processed FileContent object.
    """
    if file_content.path.suffix == '.md':
        # Remove enclosing code block syntax for Markdown files
        try:
            start = file_content.content.index("```markdown") + len("```markdown")
            end = file_content.content.rindex("```")
            processed_content = file_content.content[start:end].strip()
        except ValueError:
            processed_content = file_content.content
        processed_content = unescape_code_blocks(processed_content)
        extra_content = ""
    else:
        # Handle non-Markdown files
        try:
            start = file_content.content.index("```") + 3
            end_of_start_line = file_content.content.index('\n', start)
            start_content = end_of_start_line + 1
            end = file_content.content.index("```", start_content)
            processed_content = file_content.content[start_content:end].strip()
            extra_content = file_content.content[:start] + file_content.content[end+3:]
        except ValueError:
            processed_content = file_content.content
            extra_content = ""

    return FileContent(path=file_content.path, content=processed_content, extra_content=extra_content)

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
    base_path = base_path or Path.cwd()

    # Step 1: Parse Markdown content to get file paths and contents
    file_contents = create_file_contents_from_markdown(markdown_content, base_path)

    # Step 2: Post-process each FileContent object (e.g., unescape code blocks in Markdown)
    postprocessed_contents = [postprocess_content(fc) for fc in file_contents]

    # Step 3: Write the content of each FileContent object to the filesystem
    write_files(postprocessed_contents)
