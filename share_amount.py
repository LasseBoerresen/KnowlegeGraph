from __future__ import annotations
from dataclasses import dataclass


from ratio_range import RatioRange


@dataclass(frozen=True)
class ShareAmount:
    value: RatioRange

    def __post_init__(self):
        if not (0 <= self.value.lower.value <= 1 and 0 <= self.value.upper.value <= 1):
            raise ValueError(f"{ShareAmount.__name__} values must be between 0 and 1 inclusive")


    @classmethod
    def from_exact(cls, value: float):
        return ShareAmount(RatioRange.from_exact(value))

    def __add__(self, other: ShareAmount) -> ShareAmount:
        return ShareAmount(self.value + other.value)

    def __mul__(self, other: ShareAmount) -> ShareAmount:
        return ShareAmount(self.value * other.value)

    def __str__(self):
        return f"{self.value}"


