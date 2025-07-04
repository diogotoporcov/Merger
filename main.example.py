from pathlib import Path

import custom_readers
from merger.files import merge

if __name__ == "__main__":
    root = Path("path/to/dir")
    ignore_patterns = [
        "README.md",
        ".idea",
        "__pycache__",
        ".env",
        "./example/path",  # File or folder named 'path' relative ./example/, where '.' is the root dir
        "C:/Users/User/Desktop/path/to/dir/2",
        "output.txt",
        ".venv",
        "*.docx",  # Any file with extension .docx
        "*cache*",  # Any file of folder that contains 'cache' in its name or path
        "__*__"  # Any file or folder that starts with '__' and ends with '__'
    ]
    output_path = Path("./output.txt")

    merge(
        root,
        ignore_patterns,
        output_path,
        validation_func_override=custom_readers.validators,
        read_func_override=custom_readers.readers
    )
