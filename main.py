import json
from pathlib import Path
from pprint import pprint

from knowledge_graph import KnowledgeGraphSparseDictImpl
from share import Share
from share_dto import ShareDto


def main():
    filepath = Path('data/ResightsApS.json')
    shares = read_shares_from(filepath)

    pprint(shares)

    # kg = KnowledgeGraphSparseDictImpl.create_from(shares)
    # kg.compute_real_shares()

    # TODO: be careful when calculating mean share.. Could be different than just  min+max/2,
    #  but maybe all averages should be aggregated.


def read_shares_from(filepath: Path) -> list[Share]:
    share_dtos = read_share_dtos_from(filepath)
    throw_for_duplicated_ownership_shares(share_dtos)

    return [dto.to_domain() for dto in share_dtos]


def throw_for_duplicated_ownership_shares(shares: [ShareDto]) -> None:
    if len(set(share.id for share in shares)) != len(shares):
        raise Exception('There are multiple shares with the same id')


def read_share_dtos_from(filepath) -> list[ShareDto]:
    return [ShareDto(**sd) for sd in read_share_dtos_as_dicts_from(filepath)]


def read_share_dtos_as_dicts_from(filepath) -> list[dict]:
    with open(filepath, 'r', encoding="UTF-8") as f:
        return json.load(f)


if __name__ == "__main__":
    main()