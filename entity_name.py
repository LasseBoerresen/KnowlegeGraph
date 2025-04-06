from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EntityName:
    value: str

    def __repr__(self):
        return f"'{self.value}'"