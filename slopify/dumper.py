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
    Escape Markdown content by hiding triple backticks within unique HTML comments.
    """
    return content.replace("```", "<!--SLOPIFY_CODE_BLOCK```-->")


def dump_files_to_markdown(
    files: list[Path], output_file: Path, base_path: ty.Optional[Path] = None
):
    """
    Dump the contents of the given files to a Markdown file.

    :param files: A list of Path objects pointing to the files to be dumped.
    :param output_file: A Path object pointing to the output Markdown file.
    :param base_path: A Path object representing the base directory from
        which to calculate relative paths.
    """
    base_path = base_path or Path.cwd()
    with output_file.open("w", encoding="utf-8") as md_file:
        for file_path in sorted(files):
            # Skip the output file itself to prevent duplication
            if file_path.resolve() == output_file.resolve():
                continue

            # Calculate the relative path from the base directory
            relative_path = file_path.relative_to(base_path)

            # Write the relative path as a heading, wrapped in backticks to denote code
            md_file.write(f"# `{relative_path}`\n\n")

            # Determine the language identifier, if any
            language = get_language_from_extension(file_path.suffix.lstrip("."))

            # Attempt to read the file content
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # If a UnicodeDecodeError occurs, handle the file as binary
                content = "<binary file content not shown>"

            # If the file is a Markdown file, escape its content
            if file_path.suffix == ".md":
                content = escape_markdown_content(content)

            # Start the code block with language identifier, if applicable
            md_file.write(f"```{language}\n")

            # Write the file contents
            md_file.write(content)

            # End the code block
            md_file.write("\n```\n\n")
