from __future__ import annotations
from dataclasses import dataclass


from ratio_range import RatioRange


@dataclass(frozen=True)
class ShareAmount:
    value: RatioRange

    @classmethod
    def from_exact(cls, value: float):
        return ShareAmount(RatioRange.from_exact(value))

    def __add__(self, other: ShareAmount) -> ShareAmount:
        return ShareAmount(self.value + other.value)

    def __mul__(self, other: ShareAmount) -> ShareAmount:
        return ShareAmount(self.value * other.value)

    def __repr__(self):
        return f"{self.value}"


