from __future__ import annotations

from dataclasses import dataclass

from ratio import Ratio


@dataclass(frozen=True)
class RatioRange:
    lower: Ratio
    upper: Ratio

    def average(self) -> Ratio:
        return Ratio((self.lower.value + self.upper.value) / 2)

    @classmethod
    def from_pct(cls, lower: float, upper: float) -> RatioRange:
        return RatioRange(
            lower=Ratio.from_pct(lower),
            upper=Ratio.from_pct(upper))

    @classmethod
    def from_exact(cls, value: float):
        return RatioRange(
            lower=Ratio(value),
            upper=Ratio(value))

    def is_fraction(self) -> bool:
        return self.lower.is_fraction() and  self.upper.is_fraction()

    def __add__(self, other: RatioRange) -> RatioRange:
        return RatioRange(self.lower + other.lower, self.upper + other.upper)

    def __mul__(self, other: RatioRange) -> RatioRange:
        return RatioRange(self.lower * other.lower, self.upper * other.upper)

    def __str__(self):
        return f"({self.lower}, {self.upper})"
