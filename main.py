import json
from pathlib import Path
from pprint import pprint

import share
from entity import Entity
from share_graph import ShareGraphSparseDictImpl
from share import Share
from share_dto import ShareDto


def main():
    filepath = Path('data/CasaAS.json')
    shares = read_shares_from(filepath)

    focus_entity = read_focus_entity_from(filepath)
    pprint(focus_entity)

    # pprint(shares)


    sg = ShareGraphSparseDictImpl.create_from(shares)
    real_shares_dict = sg.compute_real_shares_in(focus_entity)

    for source, real_share in real_shares_dict.items():
        print(f"{real_share}: {source}")

    # TODO: be careful when calculating mean share.. Could be different than just  min+max/2,
    #  but maybe all averages should be aggregated.


def read_shares_from(filepath: Path) -> list[Share]:
    share_dtos = read_share_dtos_from(filepath)
    throw_for_duplicated_ownership_shares(share_dtos)

    return [dto.to_domain() for dto in share_dtos if dto.target_depth >= 0]


def throw_for_duplicated_ownership_shares(shares: [ShareDto]) -> None:
    if len(set(share.id for share in shares)) != len(shares):
        raise Exception('There are multiple shares with the same id')


def read_focus_entity_from(filepath: Path) -> Entity:
    # TODO: remove duplication in finding focus
    return focus_as_target_from(filepath) if not None else focus_as_source_from(filepath)


def focus_as_target_from(filepath):
    return next(
        (
            share_dto.to_domain().target
            for share_dto in read_share_dtos_from(filepath)
            if share_dto.target_depth == 0),
        None)

def focus_as_source_from(filepath):
    return next(
        (
            share_dto.to_domain().source
            for share_dto in read_share_dtos_from(filepath)
            if share_dto.source_depth == 0),
        None)

def read_share_dtos_from(filepath) -> list[ShareDto]:
    return [ShareDto(**sd) for sd in read_share_dtos_as_dicts_from(filepath)]


def read_share_dtos_as_dicts_from(filepath) -> list[dict]:
    with open(filepath, 'r', encoding="UTF-8") as f:
        return json.load(f)


if __name__ == "__main__":
    main()