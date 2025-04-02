from typing import Optional

from pydantic import BaseModel


class OwnershipShareEdgeDto(BaseModel):
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
