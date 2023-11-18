import pytest
from slopify.applier import apply_markdown, FileContent, write_files
from pathlib import Path


@pytest.fixture
def markdown_content_basic():
    return """
# test_basic.py

```
print('Hello, world!')
```
"""


@pytest.fixture
def markdown_content_multiple_files():
    return """
# test_file1.py

```
print('File 1 contents')
```

# test_file2.py

```
print('File 2 contents')
```
"""


def test_apply_markdown_basic(tmp_path, markdown_content_basic):
    apply_markdown(markdown_content_basic, base_path=tmp_path)
    output_file = tmp_path / "test_basic.py"
    assert output_file.read_text(encoding="utf-8") == "print('Hello, world!')"


def test_apply_markdown_multiple_files(tmp_path, markdown_content_multiple_files):
    apply_markdown(markdown_content_multiple_files, base_path=tmp_path)
    output_file1 = tmp_path / "test_file1.py"
    output_file2 = tmp_path / "test_file2.py"
    assert output_file1.read_text(encoding="utf-8") == "print('File 1 contents')"
    assert output_file2.read_text(encoding="utf-8") == "print('File 2 contents')"


def test_apply_markdown_empty_code_block(tmp_path):
    markdown_content_empty = """
# test_empty.py

```

```
"""
    apply_markdown(markdown_content_empty, base_path=tmp_path)
    output_file = tmp_path / "test_empty.py"
    assert output_file.read_text(encoding="utf-8") == ""


def test_apply_markdown_nested_structure(tmp_path):
    markdown_content_nested = """
# nested/nested_file.py

```
print('Nested file')
```

# nested/subdir/subdir_file.py

```
print('Subdir file')
```
"""
    apply_markdown(markdown_content_nested, base_path=tmp_path)
    nested_file = tmp_path / "nested" / "nested_file.py"
    subdir_file = tmp_path / "nested" / "subdir" / "subdir_file.py"
    assert nested_file.read_text() == "print('Nested file')"
    assert subdir_file.read_text() == "print('Subdir file')"


# Test for writing files with nested Markdown content
def test_write_files_nested_markdown():
    """
    Test that write_files correctly writes the content for Markdown files,
    including unescaping any nested code blocks.
    """
    # FileContent with nested code blocks marked for unescaping
    file_content = FileContent(
        path=Path("nested_markdown.md"),
        content="""
# Example Markdown Content

This is a Markdown file with nested code blocks.

<!--SLOPIFY_CODE_BLOCK```python-->
# This is a nested code block
print("Hello, nested world!")
<!--SLOPIFY_CODE_BLOCK```-->
""",
    )
    write_files([file_content])
    # Read the file and check the content
    written_content = Path("nested_markdown.md").read_text()
    assert "```python" in written_content
    assert 'print("Hello, nested world!")' in written_content
