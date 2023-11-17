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
    return content.replace("```", "<!--SLOPIFY_CODE_BLOCK```-->")

def dump_files_to_markdown(
    files: list[Path], output_file: ty.Optional[Path], base_path: ty.Optional[Path] = None
) -> str:
    base_path = base_path or Path.cwd()
    markdown_content = ""
    for file_path in sorted(files):
        if file_path.resolve() == output_file.resolve():
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
