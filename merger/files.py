from pathlib import Path
from typing import Callable, Dict, Optional, List

import chardet

from merger.filtering import filter_files_by_patterns
from merger.tree import generate_tree_visualizer


def is_text_file(
    file_path: Path,
    chunk_size: int = 1024,
    *,
    validation_func_override: Optional[Dict[str, Callable[[Path], bool]]] = None,
    min_encoding_detection_confidence: float = 0.8
) -> bool:
    """
    Determines whether a file is a readable text file.

    Args:
        file_path (Path): Path to the file.
        chunk_size (int): Number of bytes to read for encoding detection.
        validation_func_override (Optional[Dict[str, Callable]]): Optional map of extensions to custom validation functions.
        min_encoding_detection_confidence (float): Minimum confidence level required to consider encoding valid.

    Returns:
        bool: True if the file is detected as a text file or passes override validation, False otherwise.
    """
    try:
        if validation_func_override and callable(validation_override_func := validation_func_override.get(file_path.suffix)):
            return validation_override_func(file_path)

        with open(file_path, "rb") as file:
            chunk = file.read(chunk_size)

        result = chardet.detect(chunk)
        encoding = result.get("encoding")
        confidence = result.get("confidence", 0)

        if not encoding or confidence < min_encoding_detection_confidence:
            encoding = "utf-8"

        chunk.decode(encoding)
        return True

    except Exception:
        return False


def append_content(
    root: Path,
    file_path: Path,
    output_path: Path,
    *,
    prefix: str = "<<FILE_START: {path}>>\n",
    suffix: str = "\n<<FILE_END: {path}>>\n\n",
    read_func_override: Optional[Dict[str, Callable[[Path], str]]] = None,
    write_if_empty: bool = False
) -> None:
    """
    Appends file content to the output file.

    Args:
        root (Path): Root directory used for relative path resolution.
        file_path (Path): Path to the file being appended.
        output_path (Path): Output file to which content will be written.
        prefix (str): Prefix marker format with placeholder `{path}`.
        suffix (str): Suffix marker format with placeholder `{path}`.
        read_func_override (Optional[Dict[str, Callable]]): Optional map of extensions to custom read functions.
        write_if_empty (bool): Whether to include empty files in the output.
    """
    relative_path = ".\\" + str(file_path.relative_to(root))
    formatted_prefix = prefix.format(path=relative_path)
    formatted_suffix = suffix.format(path=relative_path)

    if read_func_override and callable(read_override_func := read_func_override.get(file_path.suffix)):
        content = read_override_func(file_path)

    else:
        content = file_path.read_text(encoding="utf-8")

    if not write_if_empty and not content:
        return

    with output_path.open("a", encoding="utf-8") as f:
        f.write(formatted_prefix + content + formatted_suffix)


def merge(
        dir_path: Path,
        ignore_patterns: List[str],
        output_path: Path,
        *,
        validation_func_override: Optional[Dict[str, Callable[[Path], bool]]] = None,
        read_func_override: Optional[Dict[str, Callable[[Path], str]]] = None,
        min_encoding_detection_confidence: float = 0.8,
        write_if_empty: bool = False
) -> None:
    """
    Recursively merges readable files into a single output file, with a tree visualization and optional overrides.

    Args:
        dir_path (Path): Directory to scan files from.
        ignore_patterns (List[str]): List of glob-style patterns to exclude files and directories.
        output_path (Path): File path where the output should be written.
        validation_func_override (Optional[Dict[str, Callable]]): Optional map of extensions to custom validation functions.
        read_func_override (Optional[Dict[str, Callable]]): Optional map of extensions to custom read functions.
        min_encoding_detection_confidence (float): Minimum confidence level required to consider encoding valid.
        write_if_empty (bool): Whether to include empty files in the output.
    """
    paths = filter_files_by_patterns(dir_path, ignore_patterns, True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"{generate_tree_visualizer(dir_path, paths)}\n")

    for path in paths:
        if not is_text_file(
                path,
                validation_func_override=validation_func_override,
                min_encoding_detection_confidence=min_encoding_detection_confidence
        ):
            continue

        append_content(dir_path, path, output_path, read_func_override=read_func_override, write_if_empty=write_if_empty)
