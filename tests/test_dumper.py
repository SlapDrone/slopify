from pathlib import Path
import pytest
from slopify.dumper import dump_files_to_markdown, get_language


@pytest.fixture
def test_files(tmp_path):
    # Set up a directory with some test files
    d = tmp_path / "test_dir"
    d.mkdir()
    file_basic = d / "test_basic.py"
    file_basic.write_text("print('Hello, world!')")
    file_empty = d / "test_empty.py"
    file_empty.write_text("")
    return [file_basic, file_empty]


@pytest.fixture
def nested_test_files(tmp_path):
    # Create a nested directory structure with test files
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()
    sub_dir = nested_dir / "subdir"
    sub_dir.mkdir()
    file_nested = nested_dir / "nested_file.py"
    file_nested.write_text("print('Nested file')")
    file_subdir = sub_dir / "subdir_file.py"
    file_subdir.write_text("print('Subdir file')")
    return [file_nested, file_subdir]


def test_dump_files_to_markdown(test_files, tmp_path):
    output_md = tmp_path / "output.md"
    base_path = test_files[0].parent.parent
    dump_files_to_markdown(test_files, output_md, base_path=base_path)
    expected_content = ""
    for file in sorted(test_files, key=lambda x: x.relative_to(base_path)):
        relative_path = file.relative_to(base_path)
        language = get_language(file)
        expected_content += (
            f"# `{relative_path}`\n\n"  # Include backticks around the relative path
            f"```{language}\n"
            f"{file.read_text(encoding='utf-8')}\n"
            "```\n\n"
        )
    actual_content = output_md.read_text(encoding="utf-8")
    assert actual_content == expected_content


def test_dump_files_to_markdown_empty_file(tmp_path):
    file_empty = tmp_path / "test_empty.py"
    file_empty.touch()
    output_md = tmp_path / "output_empty.md"
    base_path = file_empty.parent
    dump_files_to_markdown([file_empty], output_md, base_path=base_path)
    relative_file_path = file_empty.name
    expected_content = (
        f"# `{relative_file_path}`\n\n"  # Include backticks around the file name
        "```python\n"
        "\n"
        "```\n\n"
    )
    actual_content = output_md.read_text(encoding="utf-8")
    assert actual_content == expected_content


def test_dump_files_to_markdown_nested_structure(nested_test_files, tmp_path):
    output_md = tmp_path / "output_nested.md"
    base_path = tmp_path
    dump_files_to_markdown(nested_test_files, output_md, base_path=base_path)
    expected_content = ""
    for file in sorted(nested_test_files, key=lambda x: x.relative_to(base_path)):
        relative_path = file.relative_to(base_path)
        language = get_language(file)
        expected_content += (
            f"# `{relative_path}`\n\n"  # Include backticks around the relative path
            f"```{language}\n"
            f"{file.read_text(encoding='utf-8')}\n"
            "```\n\n"
        )
    actual_content = output_md.read_text(encoding="utf-8")
    assert actual_content == expected_content


def test_get_language_from_extension():
    # Test the language detection from file extension
    assert (
        get_language(Path("a.py")) == "python"
    )  # Remove the dot from the extension
    assert get_language(Path("b.js")) == "javascript"
    # Add more assertions for different extensions
