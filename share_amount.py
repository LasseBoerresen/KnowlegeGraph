from __future__ import annotations
from dataclasses import dataclass


from ratio_range import RatioRange


@dataclass(frozen=True)
class ShareAmount:
    value: RatioRange

    def throw_if_not_faction(self) -> ShareAmount:
        if not self.value.is_fraction():
            raise ValueError(f"{ShareAmount.__name__} values must be between {0:.1f} and {1:.1f} inclusive, got: {self.value}")

        return self

    @classmethod
    def from_exact(cls, value: float):
        return ShareAmount(RatioRange.from_exact(value))

    def __add__(self, other: ShareAmount) -> ShareAmount:
        return ShareAmount(self.value + other.value)

    def __mul__(self, other: ShareAmount) -> ShareAmount:
        return ShareAmount(self.value * other.value)

    def __str__(self):
        return f"{self.value}"
