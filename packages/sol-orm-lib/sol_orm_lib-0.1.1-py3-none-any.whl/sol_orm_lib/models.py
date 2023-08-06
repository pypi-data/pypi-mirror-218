from typing import List
from pydantic import BaseModel

# =========================================================================== #
#  TICs
# =========================================================================== #
class TACs(BaseModel):
    k: int
    ktic: str
    n: int
    timestamp: int

class TICs(BaseModel):
    timestamp: int
    pvPlannedDown: bool
    stgPlannedDown: bool
    allPlannedDown: bool
    taCs: List[TACs]
