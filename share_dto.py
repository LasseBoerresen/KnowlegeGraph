from __future__ import annotations

import json
import re
from typing import Optional
from pydantic import BaseModel

from depth import Depth
from entity_id import EntityId
from entity_name import EntityName
from entity import Entity
from ratio import Ratio
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
            source_depth=Depth(self.source_depth),
            target=Entity(EntityId(self.target), EntityName(self.target_name)),
            amount=self.__share_amount_to_domain(),
            active=self.active,
            target_depth=Depth(self.target_depth))

    def to_json(self) -> dict:
        return self.model_dump()

    def with_real_share_amount_from(self, entity_and_real_share_amounts_dict: dict[Entity, ShareAmount]) -> ShareDto:
        if not self.active:
            return self.model_copy()

        real_share_amount = entity_and_real_share_amounts_dict[self.__get_queried_entity()]

        return self.model_copy(update={
            "real_lower_share": self.__pct_str_from(real_share_amount.value.lower),
            "real_average_share": self.__pct_str_from(real_share_amount.value.average()),
            "real_upper_share": self.__pct_str_from(real_share_amount.value.upper)})

    def __get_queried_entity(self):
        if self.target_depth >= 0:
            query_entity = self.to_domain().source
        else:
            query_entity = self.to_domain().target
        return query_entity

    @staticmethod
    def __pct_str_from(ratio: Ratio) -> str:
        if ratio < Ratio(0.05):
            return "<5%"

        return f"{ratio.to_percentage_str()}%"

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
