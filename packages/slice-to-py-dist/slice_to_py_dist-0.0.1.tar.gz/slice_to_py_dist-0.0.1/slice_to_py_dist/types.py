import dataclasses
from typing import List


class SliceToPyDistError(Exception):
    pass


@dataclasses.dataclass
class DistPackageInfo:
    name: str
    version: str
    authors: List[str]
    summary: str
    requires_python: str
