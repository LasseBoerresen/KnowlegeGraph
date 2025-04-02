import json
from pprint import pprint

from owernership_share_edge_dto import OwnershipShareEdgeDto


def main():
    filepath = 'data/CasaAS.json'
    edges = load_ownership_share_edges(filepath)

    pprint([edge for edge in edges])


def load_ownership_share_edges(filepath):
    with open(filepath, 'r') as f:
        edges_as_dict = json.load(f)
        edges = [OwnershipShareEdgeDto(**edge_dict) for edge_dict in edges_as_dict if edge_dict]

    # TODO: Ask about how to interpret inactive edges. You don't show them in your image
    active_edges = [edge for edge in edges if edge.active is True]

    return active_edges


if __name__ == "__main__":
    main()