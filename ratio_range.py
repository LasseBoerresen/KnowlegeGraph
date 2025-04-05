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
