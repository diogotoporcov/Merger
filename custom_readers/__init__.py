import importlib
import pkgutil
import types
from pathlib import Path
from typing import Dict, Callable

__all__: list[str] = []

readers: Dict[str, Callable[[Path], str]] = {}
validators: Dict[str, Callable[[Path], bool]] = {}

for _, module_name, _ in pkgutil.iter_modules(__path__):
    full_name: str = f"{__name__}.{module_name}"
    module: types.ModuleType = importlib.import_module(full_name)

    if (
        hasattr(module, "ignore") and module.ignore is True
        or not hasattr(module, "reader")
        or not hasattr(module, "validator")
    ):
        continue

    key = f".{module_name}"
    readers[key] = getattr(module, "reader")
    validators[key] = getattr(module, "validator")
    __all__.append(module_name)
