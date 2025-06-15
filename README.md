# Merger

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Merger** is a flexible tool that scans a directory, filters files using customizable patterns, and merges readable content into a single output file. It implements a modular approach to custom file extensions, such as PDF files.

---

## Features

- Glob-style ignore patterns (`*.docx`, `__pycache__`, `*cache*`, etc.)
- Modular read and validation function overrides for custom files (e.g., for `.pdf`)
- Directory structure tree visualization
- Clear file content boundaries with custom prefixes and suffixes

---

## Getting Started

### Installation

1. **Clone the repository** \
   Download the project files by cloning the repository:

   ```bash
   git clone https://github.com/your-username/merger.git
   ```

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
* The output file
* File type behavior using validation/read overrides

---

## Project Structure

```
Merger/
├── custom_readers/           # Custom readers (e.g., PDF)
│   └── pdf.py
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
|----------------------------|-------------------------------------|---------------------------------------------------------|
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
    ├── files.py
    ├── filtering.py
    └── tree.py

<<FILE_START: .\merger\files.py>>
# ... file content ...
<<FILE_END: .\merger\files.py>>
```

---

## Adding Support for New File Types

To handle a new format (e.g., `.xml`):

1. Implement a reader and validation function:
   `custom_readers/xml.py`

2. Register validation function in `merge()` or `is_text_file()` call

3. Register reader function in `merge()` or `append_content()` call
 
```python
from custom_readers.xml import read_xml, is_xml_valid  

read_func_override = {".xml": read_xml},
validation_func_override = {".xml": is_xml_valid}
```

---

## Dependencies

* [`chardet`](https://github.com/chardet/chardet) – for encoding detection
* [`pymupdf`](https://github.com/pymupdf/PyMuPDF) – *optional*, only required for extracting text from PDFs

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.