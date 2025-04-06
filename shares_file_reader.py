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

    @classmethod
    def read_focus_entity_from(cls, filepath: Path) -> Entity:
        # TODO: remove duplication in finding focus

        reader = cls(filepath)
        return reader.__read_focus_as_target() if not None else reader.__read_focus_as_source()

    @staticmethod
    def __throw_for_duplicated_ownership_shares(shares: list[ShareDto]) -> None:
        if len(set(share.id for share in shares)) != len(shares):
            raise Exception('There are multiple shares with the same id')

    def __read_focus_as_target(self):
        return next(
            (
                share_dto.to_domain().target
                for share_dto in self.__read_share_dtos()
                if share_dto.target_depth == 0),
            None)

    def __read_focus_as_source(self):
        return next(
            (
                share_dto.to_domain().source
                for share_dto in self.__read_share_dtos()
                if share_dto.source_depth == 0),
            None)

    def __read_share_dtos(self) -> list[ShareDto]:
        return [ShareDto(**sd) for sd in self.__read_share_dtos_as_dicts()]

    def __read_share_dtos_as_dicts(self) -> list[dict]:
        with open(self.filepath, 'r', encoding="UTF-8") as f:
            return json.load(f)
