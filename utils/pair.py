from typing import *
from utils.configured_base_model import PyBaseModel


class Pair(PyBaseModel):
    """Utility class to store paired data"""

    s: Any
    t: Any

    def __init__(self, s: Any, t: Any):
        super().__init__()
        self.s = s
        self.t = t

    def __eq__(self, other) -> bool:
        if (isinstance(other, Pair)):
            return self.getFst() == other.getFst() and self.getSnd() == other.getSnd()

        return False

    def __str__(self):
        return str(self.s) + ", " + str(self.t)

    def __repr__(self):
        return str(self.s) + ", " + str(self.t)

    def getFst(self) -> Any:
        return self.s

    def setFst(self, s: Any) -> None:
        self.s = s

    def getSnd(self) -> Any:
        return self.t

    def setSnd(self, t) -> None:
        self.t = t
