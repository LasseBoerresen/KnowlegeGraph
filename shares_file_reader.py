import json
from pathlib import Path

from entity import Entity
from share import Share
from share_amount import ShareAmount
from share_dto import ShareDto


class SharesFileReader:
    def __init__(self, filepath):
        self.filepath = filepath

    @classmethod
    def read_shares_from(cls, filepath: Path) -> list[ShareDto]:
        reader = cls(filepath)
        share_dtos = reader.__read_share_dtos()
        reader.__throw_for_duplicated_ownership_shares(share_dtos)

        return share_dtos

    @classmethod
    def write_real_shares_to(cls, filepath: Path, entity_and_real_share_amount_dict: dict[Entity, ShareAmount]) -> None:
        reader = cls(filepath)

        share_dtos_with_real_amounts = [
            share_dto.with_real_share_amount_from(entity_and_real_share_amount_dict)
            for share_dto in reader.__read_share_dtos()]

        reader.__write_share_dtos(share_dtos_with_real_amounts)

    def __write_share_dtos(self, share_dtos: list[ShareDto]) -> None:
        self.__write_share_dtos_from_dicts([share_dto.to_json() for share_dto in share_dtos])

    def __write_share_dtos_from_dicts(self, share_dto_as_json: list[dict]) -> None:
        with open(self.filepath, 'w', encoding="UTF-8") as f:
            json.dump(share_dto_as_json, f, indent=4, ensure_ascii=False)

    def __read_share_dtos(self) -> list[ShareDto]:
        return [ShareDto(**sd) for sd in self.__read_share_dtos_as_dicts()]

    def __read_share_dtos_as_dicts(self) -> list[dict]:
        with open(self.filepath, 'r', encoding="UTF-8") as f:
            return json.load(f)

    @staticmethod
    def __throw_for_duplicated_ownership_shares(shares: list[ShareDto]) -> None:
        if len(set(share.id for share in shares)) != len(shares):
            raise Exception('There are multiple shares with the same id')
