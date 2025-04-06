# tests/test_share_graph.py
from collections import namedtuple

import pytest

from entity import Entity
from entity_id import EntityId
from entity_name import EntityName
from share import Share
from share_amount import ShareAmount
from share_graph import ShareGraphSparseDictImpl


from typing import NamedTuple


class TestInput(NamedTuple):
    shares: list[Share]
    entity_in_focus: Entity
    entity_queried: Entity
    expected_real_share_amount: ShareAmount


class TestShareGraph:

    @staticmethod
    def create_test_entity(entity_id: int):
        return Entity(id=EntityId(entity_id), name=EntityName(f"{entity_id}"))


    e0 = create_test_entity(0)
    e1 = create_test_entity(1)

    @pytest.mark.parametrize(
        "shares, entity_in_focus, entity_queried, expected_real_share_amount",
        [
            TestInput(
                [Share(source=e1, target=e0, amount=ShareAmount.from_exact(1.0), active=True)],
                e0,
                e1,
                ShareAmount.from_exact(1.0)),
            TestInput(
                [Share(source=e1, target=e0, amount=ShareAmount.from_exact(0.5), active=True)],
                e0,
                e1,
                ShareAmount.from_exact(0.5)),
        ])
    def test_given_shares_and_focus_and_queried_entity__when_get_real_share__then_returns_expected(
            self,
            shares: list[Share],
            entity_in_focus: Entity,
            entity_queried: Entity,
            expected_real_share_amount: ShareAmount):
        # Given
        graph = ShareGraphSparseDictImpl.create_from(shares)

        # When
        actual_real_share_amount = graph.real_share_amounts_for(
            source=entity_queried.id, focus=entity_in_focus.id)

        # Then
        assert actual_real_share_amount == expected_real_share_amount



if __name__ == '__main__':
    pytest.main()