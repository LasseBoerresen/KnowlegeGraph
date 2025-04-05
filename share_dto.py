import re
from typing import Optional
from pydantic import BaseModel
from entity_id import EntityId
from entity_name import EntityName
from entity import Entity
from share import Share
from ratio_range import RatioRange
from share_amount import ShareAmount


class ShareDto(BaseModel):
    id: str
    source: int
    source_name: str
    source_depth: int
    target: int
    target_name: str
    target_depth: int
    share: str
    real_lower_share: Optional[str]
    real_average_share: Optional[str]
    real_upper_share: Optional[str]
    active: bool

    def to_domain(self) -> Share:
        return Share(
            source=Entity(EntityId(self.source), EntityName(self.source_name)),
            target=Entity(EntityId(self.target), EntityName(self.target_name)),
            amount=self.__share_amount_to_domain(),
            active=self.active)

    def __share_amount_to_domain(self) -> ShareAmount:
        if "-" in self.share:
            return self.__share_amount_from_range_str()
        elif "<" in self.share:
            return self.__share_amount_from_less_than_str()
        else:
            return self.__share_amount_from_exact_value_str()

    def __share_amount_from_range_str(self) -> ShareAmount:
        match = re.match(pattern=r"(\d+)-(\d+)", string=self.share)

        ratio_range = RatioRange.from_pct(int(match.group(1)), int(match.group(2)))

        return ShareAmount(ratio_range)

    def __share_amount_from_less_than_str(self) -> ShareAmount:
        match = re.match(pattern=r"<(\d+)", string=self.share)

        ratio_range = RatioRange.from_pct(0.0, int(match.group(1)))

        return ShareAmount(ratio_range)

    def __share_amount_from_exact_value_str(self) -> ShareAmount:
        match = re.match(pattern=r"(\d+)", string=self.share)

        ratio_range = RatioRange.from_pct(int(match.group(1)), int(match.group(1)))

        return ShareAmount(ratio_range)
