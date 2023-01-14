from typing import *
from pydantic import BaseModel


class Pair(BaseModel):
    """Utility class to store paired data"""

    s: Any
    t: Any

    class Config:
        validate_assignment = True
        allow_mutation = True

    def __init__(self, s: Any, t: Any, **data: Any):
        super().__init__(**data)
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
