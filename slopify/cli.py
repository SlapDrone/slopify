import typer
from .dumper import dump_files_to_markdown
from .applier import apply_markdown
from pathlib import Path
import pathspec
import pyperclip

app = typer.Typer()


def load_gitignore_patterns(directory: Path) -> pathspec.PathSpec:
    gitignore = directory / ".gitignore"
    patterns = ["/.git/", "*/.git/", "**/.git/", "LICENSE*"]
    if gitignore.exists():
        patterns += gitignore.read_text().splitlines()
    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return spec


@app.command()
def slop(
    paths: list[Path] = typer.Argument(
        ..., help="List of file paths or directories to dump.", exists=True
    ),
    output: Path = typer.Option(
        None, "--output", "-o", help="Output Markdown file name."
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Recursively include files from subdirectories.",
    ),
):
    gitignore_spec = load_gitignore_patterns(Path.cwd())
    files_to_dump = []
    for path in paths:
        path = path.resolve()
        if path.is_dir():
            if recursive:
                files = path.rglob("*")
            else:
                files = path.glob("*")
            for file in files:
                if file.is_file() and not gitignore_spec.match_file(file):
                    files_to_dump.append(file.resolve())
        elif path.is_file() and not gitignore_spec.match_file(path):
            files_to_dump.append(path.resolve())

    if output:
        output = output.resolve()
        files_to_dump = [f for f in files_to_dump if f != output]
        base_path = Path.cwd()
        dump_files_to_markdown(files_to_dump, output, base_path=base_path)
        typer.echo(f"Dumped contents to {output}")
    else:
        markdown_content = dump_files_to_markdown(
            files_to_dump, None, base_path=Path.cwd()
        )
        pyperclip.copy(markdown_content)
        typer.echo("Copied contents to clipboard")


@app.command()
def slather(
    markdown_file: Path = typer.Option(
        None, "--input", "-i", help="Markdown file containing the code to apply."
    )
):
    if markdown_file:
        apply_markdown(markdown_file)
        typer.echo(f"Applied code from {markdown_file}")
    else:
        markdown_content = pyperclip.paste()
        if markdown_content:
            apply_markdown(markdown_content)
            typer.echo("Applied code from clipboard")
        else:
            typer.echo("Clipboard is empty. No code was applied.", err=True)


if __name__ == "__main__":
    app()
