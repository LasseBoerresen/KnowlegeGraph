from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Ratio:
    value: float

    def is_fraction(self):
        return 0 <= self.value <= 1

    def to_percentage_str(self) -> str:
        return f"{self.value:.0%}"

    @classmethod
    def from_pct(cls, pct: float) -> Ratio:
        return Ratio(pct / 100.0)

    def __add__(self, other: Ratio) -> Ratio:
        return Ratio(self.value + other.value)

    def __mul__(self, other: Ratio) -> Ratio:
        return Ratio(self.value * other.value)

    def __lt__(self, other: Ratio) -> bool:
        return self.value < other.value

    def __str__(self):
        return f"{self.value:.3f}"

