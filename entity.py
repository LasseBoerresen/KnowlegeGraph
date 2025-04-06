from __future__ import annotations

from dataclasses import dataclass

from entity_id import EntityId
from entity_name import EntityName


@dataclass(frozen=True)
class Entity:
    id: EntityId
    name: EntityName

    def __repr__(self):
        return f"{self.name}"
