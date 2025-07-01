from pathlib import Path
from typing import Final, Callable

from custom_readers import pdf

validator: Final[Callable[[Path], bool]] = pdf.validator
reader: Final[Callable[[Path], str]] = pdf.reader

ignore = True

__all__ = ["validator", "reader"]
