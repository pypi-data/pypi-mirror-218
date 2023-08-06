from typing import TypedDict
from enum import Enum


class Subjects(Enum):
    TargetCreated = 'target.created'
    StructureComputed = 'structure.computed'


class TargetCreatedData(TypedDict):
    id: int
    custom: bool
    rna_id: str
    spliced: bool
    seq: str


class StructureComputedData(TypedDict):
    target_id: int
    id: int
    openness: list[float]
