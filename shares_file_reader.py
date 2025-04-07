import json
from pathlib import Path

from entity import Entity
from share import Share
from share_dto import ShareDto


class SharesFileReader:
    def __init__(self, filepath):
        self.filepath = filepath

    @classmethod
    def read_shares_from(cls, filepath: Path) -> list[Share]:
        reader = cls(filepath)
        share_dtos = reader.__read_share_dtos()
        reader.__throw_for_duplicated_ownership_shares(share_dtos)

        return [dto.to_domain() for dto in share_dtos]

    @staticmethod
    def __throw_for_duplicated_ownership_shares(shares: list[ShareDto]) -> None:
        if len(set(share.id for share in shares)) != len(shares):
            raise Exception('There are multiple shares with the same id')

    def __read_share_dtos(self) -> list[ShareDto]:
        return [ShareDto(**sd) for sd in self.__read_share_dtos_as_dicts()]

    def __read_share_dtos_as_dicts(self) -> list[dict]:
        with open(self.filepath, 'r', encoding="UTF-8") as f:
            return json.load(f)
