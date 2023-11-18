import pytest
from slopify.applier import *
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
    assert output_file.read_text(encoding="utf-8") == "print('Hello, world!')\n"

def test_apply_markdown_multiple_files(tmp_path, markdown_content_multiple_files):
    apply_markdown(markdown_content_multiple_files, base_path=tmp_path)
    output_file1 = tmp_path / "test_file1.py"
    output_file2 = tmp_path / "test_file2.py"
    assert output_file1.read_text(encoding="utf-8") == "print('File 1 contents')\n"
    assert output_file2.read_text(encoding="utf-8") == "print('File 2 contents')\n"

def test_apply_markdown_empty_code_block(tmp_path):
    markdown_content_empty = """
# test_empty.py

```

```
"""
    apply_markdown(markdown_content_empty, base_path=tmp_path)
    output_file = tmp_path / "test_empty.py"
    assert output_file.read_text(encoding="utf-8") == "\n"

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
    assert nested_file.read_text() == "print('Nested file')\n"
    assert subdir_file.read_text() == "print('Subdir file')\n"



# Test for parsing Markdown with nested code blocks
def test_parse_markdown_nested_code_blocks():
    """
    Test that parse_markdown correctly identifies and extracts the content
    for Markdown files with nested code blocks, ensuring that the code blocks
    are marked for unescaping.
    """
    # Markdown content with nested code blocks
    markdown_content = """
# `nested_markdown.md`

```
# Example Markdown Content

This is a Markdown file with nested code blocks.

<!--SLOPIFY_CODE_BLOCK```-->python
# This is a nested code block
print("Hello, nested world!")
<!--SLOPIFY_CODE_BLOCK```-->
```
"""
    md = MarkdownIt()
    tokens = md.parse(markdown_content)
    base_path = Path.cwd()
    file_contents = parse_markdown(tokens, base_path)
    # There should be one FileContent object
    assert len(file_contents) == 1
    # The path should be correct
    assert file_contents[0].path == base_path / "nested_markdown.md"
    # The content should include the marker for unescaping
    assert "<!--SLOPIFY_CODE_BLOCK" not in file_contents[0].content
    assert "```" in file_contents[0].content

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
"""
    )
    write_files([file_content])
    # Read the file and check the content
    written_content = Path("nested_markdown.md").read_text()
    assert "```python" in written_content
    assert "print(\"Hello, nested world!\")" in written_content

# Test for unescaping code blocks within Markdown content
def test_unescape_code_blocks():
    """
    Test that unescape_code_blocks correctly unescapes escaped code blocks
    within Markdown content.
    """
    escaped_content = """
This is a Markdown file.

<!--SLOPIFY_CODE_BLOCK\`\`\`python-->
# This is a nested code block
print("Hello, nested world!")
<!--SLOPIFY_CODE_BLOCK\`\`\`-->
"""
    unescaped_content = unescape_code_blocks(escaped_content)
    assert "```python" in unescaped_content
    assert "<!--SLOPIFY_CODE_BLOCK" not in unescaped_content

# Test for the full apply_markdown process with nested Markdown
def test_apply_markdown_with_nested_markdown(tmp_path):
    """
    Test that apply_markdown correctly processes Markdown content with nested
    Markdown files, unescaping code blocks and writing the files to the filesystem.
    """
    markdown_content = """
# `nested_markdown.md`

```
# Example Markdown Content

This is a Markdown file with nested code blocks.

\`\`\`python
# This is a nested code block
print("Hello, nested world!")
\`\`\`
```
"""
    apply_markdown(markdown_content, base_path=tmp_path)
    written_content = (tmp_path / "nested_markdown.md").read_text()
    assert "```python" in written_content
    assert "print(\"Hello, nested world!\")" in written_content
