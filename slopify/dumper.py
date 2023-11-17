import typing as ty
import os
from pathlib import Path


def get_language_from_extension(file_path: str) -> str:
    extension_to_language = {
        "py": "python",
        "js": "javascript",
        "sh": "bash",
        "md": "markdown",
        "html": "html",
        "css": "css",
        "c": "c",
        "cpp": "cpp",
        "h": "c",
        "hpp": "cpp",
        "java": "java",
        "go": "go",
        "swift": "swift",
        "scala": "scala",
        "rb": "ruby",
        "php": "php",
        "cs": "csharp",
        "fs": "fsharp",
        "ts": "typescript",
        "kt": "kotlin",
        "pl": "perl",
        # Add more mappings if needed
    }
    extension = os.path.splitext(file_path)[1].lstrip(".")
    return extension_to_language.get(extension, "")


def escape_markdown_content(content: str) -> str:
    """
    Escape triple backticks in Markdown content outside of code blocks.
    """
    escaped_content = []
    in_code_block = False
    for line in content.splitlines():
        if line.startswith("```"):
            in_code_block = not in_code_block
            escaped_content.append(line)
        elif not in_code_block:
            escaped_content.append(line.replace("```", "<!--SLOPIFY_CODE_BLOCK```-->"))
        else:
            escaped_content.append(line)
    return "\n".join(escaped_content)


def dump_files_to_markdown(
    files: list[Path],
    output_file: ty.Optional[Path],
    base_path: ty.Optional[Path] = None,
) -> str:
    """
    Dump the contents of the given files to a Markdown file or return as a string.

    :param files: A list of Path objects pointing to the files to be dumped.
    :param output_file: A Path object pointing to the output Markdown file, or None.
    :param base_path: A Path object representing the base directory from
        which to calculate relative paths.
    :return: The markdown content as a string if output_file is None, otherwise None.
    """
    base_path = base_path or Path.cwd()
    markdown_content = ""
    for file_path in sorted(files):
        # Skip the output file if it is specified and matches the current file path
        if output_file and file_path.resolve() == output_file.resolve():
            continue

        relative_path = file_path.relative_to(base_path)
        language = get_language_from_extension(file_path.suffix.lstrip("."))
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = "<binary file content not shown>"
        if file_path.suffix == ".md":
            content = escape_markdown_content(content)
        markdown_content += f"# `{relative_path}`\n\n```{language}\n{content}\n```\n\n"

    if output_file:
        with output_file.open("w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
    return markdown_content
