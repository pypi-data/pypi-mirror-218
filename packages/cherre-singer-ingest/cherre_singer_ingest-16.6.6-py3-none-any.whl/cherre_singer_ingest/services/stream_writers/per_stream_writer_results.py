from typing import Optional, List

from cherre_types import FilePath, FolderPath
from dataclasses import dataclass


@dataclass(eq=True, repr=True, frozen=True)
class PerStreamWriterResults:
    file: FilePath
    sub_folder: Optional[FolderPath]
    column_names: Optional[List[str]] = None
