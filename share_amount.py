from dataclasses import dataclass

from ratio_range import RatioRange


@dataclass(frozen=True)
class ShareAmount:
    value: RatioRange
