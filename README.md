# Merger

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Merger** is a flexible tool that scans a directory, filters files using customizable patterns, and merges readable content into a single output file. It supports automatic discovery of custom file handlers, such as for `.pdf` or `.ipynb` files.

---

## Features

- Glob-style ignore patterns (`*.docx`, `__pycache__`, `*cache*`, etc.)
- Auto-import of custom readers and validators
- Modular override support for non-standard file types
- Directory tree visualization in output
- Clear file boundaries with custom delimiters

---

## Getting Started

### Installation

1. **Clone the repository**

    ```bash
   git clone https://github.com/your-username/merger.git
    ````

2. **Navigate to the project directory**

   ```bash
   cd "C:/Users/user/Desktop/Merger"
   ```

3. **Create a virtual environment**

   * On **Linux/macOS**:

     ```bash
     python3 -m venv .venv
     ```

   * On **Windows**:

     ```bash
     python -m venv .venv
     ```

4. **Activate the virtual environment**

   * On **Linux/macOS**:

     ```bash
     source .venv/bin/activate
     ```

   * On **Windows**:

     ```bash
     .venv\Scripts\activate
     ```

5. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Example Usage

```bash
python main.example.py
```

You can customize:

* The root path to read files
* The list of ignore patterns
* The output file path
* Behavior for custom file types

---

### Auto-Import of Custom Readers

The `custom_readers/` directory supports plugin-style extensibility. Any module inside this folder will be **automatically discovered** if it defines both:

```python
validator: Callable[[Path], bool]
reader: Callable[[Path], str]
```

The module will be registered based on its filename — for example, `pdf.py` will handle files with the `.pdf` extension.

To **exclude a module** from being loaded automatically, simply add:

```python
ignore = True
```

This system allows you to add support for new file types without changing any core logic, just drop in a new module with the expected interface, and it will be picked up automatically.

---

## Project Structure

```
Merger/
├── custom_readers/           # Auto-discovered file readers (e.g., PDF, IPYNB)
│   ├── pdf.py                # Implements reader and validator for .pdf
│   ├── ipynb.py              # Implements reader and validator for .ipynb
│   └── alias.example.py      # Example of aliasing an existing reader and validation implementation
├── merger/                   # Core merger logic
│   ├── files.py              # Core merge implementation
│   ├── filtering.py          # Path filtering
│   └── tree.py               # Directory visualization
├── main.example.py           # Example usage
└── requirements.txt          # Python dependencies
```

---

## Configuration Options

### `merge(...)` arguments:

| Argument                   | Type                                | Description                                             |
| -------------------------- | ----------------------------------- | ------------------------------------------------------- |
| `dir_path`                 | `Path`                              | Directory to recursively scan                           |
| `ignore_patterns`          | `List[str]`                         | Glob-like patterns to exclude files/directories         |
| `output_path`              | `Path`                              | Path to the output `.txt` file                          |
| `validation_func_override` | `Dict[str, Callable[[Path], bool]]` | Per-extension validation for file readability           |
| `read_func_override`       | `Dict[str, Callable[[Path], str]]`  | Per-extension content reader (e.g., for `.pdf`)         |
| `write_if_empty`           | `bool`                              | Include empty files in the merged output                |
| `min_encoding_confidence`  | `float`                             | Minimum confidence for encoding detection via `chardet` |

---

## Example Output

```txt
Merger/
├── custom_readers/
│   └── pdf.py
└── merger/
    ├── sentences.py
    └── tree.py

<<FILE_START: .\merger\sentences.py>>
import random

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a versatile programming language loved by many.",
    "Reading books expands the mind and imagination.",
    "Traveling allows us to experience new cultures and ideas.",
    "Healthy eating contributes to a better quality of life.",
    "Music has the power to evoke strong emotions and memories.",
    "Learning new skills opens doors to new opportunities."
]

def generate_paragraph(num_sentences=5):
    return ' '.join(random.choice(sentences) for _ in range(num_sentences))

print(generate_paragraph())
<<FILE_END: .\merger\sentences.py>>

<<FILE_START: .\merger\tree.py>>
# ... file content ...
<<FILE_END: .\merger\tree.py>>
```

---

## Adding Support for New File Types

To support a new extension (e.g., `.xml`):

1. Create a file `custom_readers/xml.py`
2. Implement:

```python
from pathlib import Path
from typing import Callable, Final

def is_xml_valid(file: Path) -> bool:
    # validation logic
    ...

def read_xml(file: Path) -> str:
    # read logic
    ...

validator: Final[Callable[[Path], bool]] = is_xml_valid
reader: Final[Callable[[Path], str]] = read_xml

__all__ = ["validator", "reader"]
```

3. That’s it! The system will detect it automatically via `custom_readers.__init__.py`.

To skip registration, include `ignore = True`.

---

## Dependencies

* [`chardet`](https://github.com/chardet/chardet) – for encoding detection
* [`pymupdf`](https://github.com/pymupdf/PyMuPDF) – *optional*, only required for extracting text from PDFs

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.