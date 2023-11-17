import pytest
from slopify.applier import apply_markdown
from pathlib import Path


@pytest.fixture
def markdown_content_basic(tmp_path):
    content = """
# test_basic.py

```
print('Hello, world!')
```
"""
    markdown_file = tmp_path / "test_basic.md"
    markdown_file.write_text(content)
    return markdown_file

@pytest.fixture
def markdown_content_multiple_files(tmp_path):
    content = """
# test_file1.py

```
print('File 1 contents')
```

# test_file2.py

```
print('File 2 contents')
```
"""
    markdown_file = tmp_path / "test_multiple.md"
    markdown_file.write_text(content)
    return markdown_file

def test_apply_markdown_basic(markdown_content_basic):
    apply_markdown(markdown_content_basic)
    output_file = markdown_content_basic.parent / "test_basic.py"
    assert output_file.read_text(encoding='utf-8') == "print('Hello, world!')\n"

def test_apply_markdown_multiple_files(markdown_content_multiple_files):
    apply_markdown(markdown_content_multiple_files)
    output_file1 = markdown_content_multiple_files.parent / "test_file1.py"
    output_file2 = markdown_content_multiple_files.parent / "test_file2.py"
    assert output_file1.read_text(encoding='utf-8') == "print('File 1 contents')\n"
    assert output_file2.read_text(encoding='utf-8') == "print('File 2 contents')\n"

def test_apply_markdown_empty_code_block(tmp_path):
    markdown_content_empty = """
# test_empty.py

```

```
"""
    markdown_file = tmp_path / "test_empty.md"
    markdown_file.write_text(markdown_content_empty)
    apply_markdown(markdown_file)
    output_file = tmp_path / "test_empty.py"
    assert output_file.read_text(encoding='utf-8') == "\n"
    
def test_apply_markdown_nested_structure(tmp_path):
    markdown_content = """
# nested/nested_file.py

```
print('Nested file')
```

# nested/subdir/subdir_file.py

```
print('Subdir file')
```
"""
    markdown_file = tmp_path / "nested_structure.md"
    markdown_file.write_text(markdown_content)

    # Run the apply command to apply the Markdown content to the files
    apply_markdown(markdown_file, base_path=tmp_path)

    # Verify that the files are created with the correct nested directory structure
    nested_file = tmp_path / "nested" / "nested_file.py"
    subdir_file = tmp_path / "nested" / "subdir" / "subdir_file.py"
    assert nested_file.read_text() == "print('Nested file')\n"
    assert subdir_file.read_text() == "print('Subdir file')\n"
