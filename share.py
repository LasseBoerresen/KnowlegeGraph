from __future__ import annotations

from dataclasses import dataclass

from entity import Entity
from share_amount import ShareAmount


@dataclass(frozen=True)
class Share:
    source: Entity
    target: Entity
    amount: ShareAmount
    active: bool

    @staticmethod
    def filter_to_active_shares(shares: list[Share]) -> list[Share]:
        return [share for share in shares if share.active is True]
