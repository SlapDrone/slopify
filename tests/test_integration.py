from textwrap import dedent
import pytest
from slopify.dumper import dump_files_to_markdown
from slopify.applier import apply_markdown
from pathlib import Path
from typing import List


@pytest.fixture
def setup_test_files(tmp_path) -> List[Path]:
    # Create test files with known content
    file1 = tmp_path / "file1.py"
    file1.write_text("print('Hello, world!')")
    file2 = tmp_path / "file2.py"
    file2.write_text("print('Goodbye, world!')")
    # Create a package directory and add an __init__.py file
    package_dir = tmp_path / "package"
    package_dir.mkdir()
    init_file = package_dir / "__init__.py"
    init_file.write_text("# This is the __init__.py file")
    # Add more files to the package if needed
    file3 = package_dir / "module.py"
    file3.write_text("print('This is a module within a package')")
    # add a code file that contains triple backticks
    file4 = package_dir / "backticks.py"
    file4.write_text("print('have you tried ```bash\nsudo rm -rf /\n```?')")
    # add a markdown file with code blocks
    file5 = tmp_path / "README.md"
    file5.write_text(dedent("""\
        # introduction

        bla bla

        ```c++
        int main() {
            return 0;
        }
        ```

        # conclusion

        bleep bloop
    """))
    return [file1, file2, init_file, file3, file4, file5]


def test_vomit_apply_idempotent(setup_test_files, tmp_path):
    output_md = tmp_path / "output.md"
    base_path = tmp_path
    
    # Capture the original content of the files before applying markdown
    original_contents = {file: file.read_text() for file in setup_test_files}
    
    dump_files_to_markdown(setup_test_files, output_md, base_path=base_path)
    apply_markdown(output_md, base_path=base_path)
    
    # Verify that the files' content remains unchanged except for a possible trailing newline
    for file in setup_test_files:
        file_content = file.read_text()
        original_content = original_contents[file]
        assert file_content == original_content or file_content == original_content + '\n'

def test_apply_with_commentary_ignored(tmp_path):
    # Create a Markdown file with code blocks and extra content
    markdown_content = """
# file1.py
Some commentary before the code block.

```
print('Hello, world!')
```
Some commentary after the code block.

# file2.py
More commentary before the code block.

```
print('Goodbye, world!')
```
Even more commentary after the code block.
"""
    markdown_file = tmp_path / "slop.md"
    markdown_file.write_text(markdown_content)

    # Create the files that should be affected
    file1 = tmp_path / "file1.py"
    file1.touch()
    file2 = tmp_path / "file2.py"
    file2.touch()

    # Run the apply command to apply the Markdown content to the files
    apply_markdown(markdown_file)

    # Verify that only the content within the code blocks is applied to the files
    assert file1.read_text() == "print('Hello, world!')\n"
    assert file2.read_text() == "print('Goodbye, world!')\n"

def test_vomit_slather_escape_unescape_cycle(setup_test_files, tmp_path):
    output_md = tmp_path / "output.md"
    # The base path should be the common parent directory of the setup test files
    base_path = setup_test_files[0].parent.parent
    dump_files_to_markdown(setup_test_files, output_md, base_path=base_path)

    # Run the slather command to apply the content back to the files
    apply_markdown(output_md)

    # Verify that the files' content matches the original content, allowing for a trailing newline
    for file in setup_test_files:
        file_content = file.read_text(encoding='utf-8')
        original_content = file.read_text(encoding='utf-8')
        assert file_content == original_content or file_content == original_content + '\n'
