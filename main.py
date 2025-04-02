import json
from pprint import pprint

from knowledge_graph import KnowledgeGraphSparseDictImpl
from owernership_share_edge_dto import OwnershipShareEdgeDto


def main():
    filepath = 'data/CasaAS.json'
    edges = load_ownership_share_edges(filepath)

    KnowledgeGraphSparseDictImpl.create_from()


def load_ownership_share_edges(filepath) -> list[OwnershipShareEdgeDto]:
    edges = load_ownership_share_edges_from_file(filepath)

    # TODO: Ask about how to interpret inactive edges. You don't show them in your image
    active_edges = [edge for edge in edges if edge.active is True]

    throw_for_duplicated_ownership_shares(active_edges)

    return active_edges


def throw_for_duplicated_ownership_shares(active_edges) -> None:
    if len(set(active_edge.id for active_edge in active_edges)) != len(active_edges):
        raise Exception('There are multiple active edges with the same id')


def load_ownership_share_edges_from_file(filepath) -> list[OwnershipShareEdgeDto]:
    with open(filepath, 'r') as f:
        edges_as_dict = json.load(f)

    edges = [OwnershipShareEdgeDto(**edge_dict) for edge_dict in edges_as_dict]
    return edges


if __name__ == "__main__":
    main()