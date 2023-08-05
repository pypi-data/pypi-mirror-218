import logging
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Union, List
from truss.templates.control.control.helpers.types import Patch


class PatchApplier(ABC):
    """Abstract base class for patch applier subclasses"""

    def __init__(self, truss_dir: Path, logger: logging.Logger) -> None:
        self._truss_dir = truss_dir
        self._logger = logger

    @abstractmethod
    def __call__(self, patch: Union[List[Patch], Patch]) -> None:
        pass
