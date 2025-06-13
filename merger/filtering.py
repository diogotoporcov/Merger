from pathlib import Path
import fnmatch
from typing import List


def filter_files_by_patterns(dir_path: Path, ignore_patterns: List[str], recursive: bool) -> List[Path]:
    """
    Filters files and directories under a root directory, excluding any that match ignore patterns.

    Args:
        dir_path (Path): Directory to scan files from.
        ignore_patterns (List[str]): List of glob-style patterns to exclude files and directories.
        recursive (bool): Whether to scan directories recursively.

    Returns:
        List[Path]: A list of matching file and directory paths.
    """

    def matches_any_pattern(path: Path) -> bool:
        rel_path = path.relative_to(dir_path).as_posix()
        for pattern in ignore_patterns:
            pat = pattern.rstrip("/")
            if fnmatch.fnmatch(rel_path, pat):
                return True

            if fnmatch.fnmatch(path.name, pat):
                return True

        return False

    results = []

    def scan_dir(directory: Path):
        for entry in directory.iterdir():
            if matches_any_pattern(entry):
                continue

            results.append(entry)
            if recursive and entry.is_dir():
                scan_dir(entry)

    scan_dir(dir_path)
    return results
