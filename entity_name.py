from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EntityName:
    value: str

    def __str__(self):
        return f"'{self.value}'"