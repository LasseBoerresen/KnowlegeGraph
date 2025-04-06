from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Ratio:
    value: float

    def to_percentage_str(self) -> str:
        return f"{self.value:.1%}"

    @classmethod
    def from_pct(cls, pct: float) -> Ratio:
        return Ratio(pct / 100.0)

    def __add__(self, other: Ratio) -> Ratio:
        return Ratio(self.value + other.value)

    def __mul__(self, other: Ratio) -> Ratio:
        return Ratio(self.value * other.value)

    def __repr__(self):
        return f"{self.value}"

