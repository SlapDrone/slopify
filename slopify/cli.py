import typer
from .dumper import dump_files_to_markdown
from .applier import apply_markdown
from pathlib import Path
import pathspec

app = typer.Typer()


def load_gitignore_patterns(directory: Path) -> pathspec.PathSpec:
    gitignore = directory / ".gitignore"
    # Include the .git directory in the ignore patterns by default
    patterns = ["/.git/", "*/.git/", "**/.git/", "LICENSE*"]
    if gitignore.exists():
        patterns += gitignore.read_text().splitlines()
    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return spec


@app.command()
def vomit(
    paths: list[Path] = typer.Argument(
        ..., help="List of file paths or directories to dump.", exists=True
    ),
    output: Path = typer.Option(
        "slop.md", "--output", "-o", help="Output Markdown file name."
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Recursively include files from subdirectories.",
    ),
):
    # Resolve the output path to an absolute path
    output = output.resolve()

    # Load .gitignore patterns
    gitignore_spec = load_gitignore_patterns(Path.cwd())

    files_to_dump = []
    for path in paths:
        # Convert to absolute path
        path = path.resolve()
        if path.is_dir():
            if recursive:
                files = path.rglob("*")
            else:
                files = path.glob("*")
            for file in files:
                if file.is_file() and not gitignore_spec.match_file(file):
                    files_to_dump.append(
                        file.resolve()
                    )  # Ensure the file path is absolute
        elif path.is_file() and not gitignore_spec.match_file(path):
            files_to_dump.append(path.resolve())  # Ensure the file path is absolute

    # Filter out the output file itself
    files_to_dump = [f for f in files_to_dump if f != output]

    # The base path should be the current working directory
    base_path = Path.cwd()
    dump_files_to_markdown(files_to_dump, output, base_path=base_path)
    typer.echo(f"Dumped contents to {output}")


@app.command()
def slather(
    markdown_file: Path = typer.Argument(
        ..., help="Markdown file containing the code to apply."
    )
):
    apply_markdown(markdown_file)
    typer.echo(f"Applied code from {markdown_file}")


if __name__ == "__main__":
    app()
