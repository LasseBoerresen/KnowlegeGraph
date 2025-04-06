# tests/test_share_graph.py
from collections import namedtuple

import pytest

from depth import Depth
from entity import Entity
from entity_id import EntityId
from entity_name import EntityName
from share import Share
from share_amount import ShareAmount
from share_graph import ShareGraphSparseDictImpl


from typing import NamedTuple


class TestInput(NamedTuple):
    shares: list[Share]
    entity_queried: Entity
    entity_in_focus: Entity
    expected_real_share_amount: ShareAmount


class TestShareGraph:

    @staticmethod
    def create_test_entity(entity_id: int):
        return Entity(id=EntityId(entity_id), name=EntityName(f"{entity_id}"))

    e0 = create_test_entity(0)
    e1 = create_test_entity(1)
    e2 = create_test_entity(2)

    @pytest.mark.parametrize(
        "shares, entity_queried, entity_in_focus, expected_real_share_amount",
        [
            # Single 100% share
            # Then: 100%
            TestInput(
                shares=[Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0), active=True)],
                entity_queried=e1,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(1.0)),

            # Given: Single 50% share
            # Then:  50%
            TestInput(
                shares=[Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e1,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.5)),

            # Given: two 50% shares in serial
            # Then:  25%
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e2,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.25)),
        ])
    def test_given_shares_and_focus_and_queried_entity__when_get_real_share__then_returns_expected(
            self,
            shares: list[Share],
            entity_queried: Entity,
            entity_in_focus: Entity,
            expected_real_share_amount: ShareAmount):
        # Given
        graph = ShareGraphSparseDictImpl.create_from(shares)

        # When
        actual_real_share_amount = graph.real_share_amounts_for(
            source=entity_queried, focus=entity_in_focus)

        # Then
        assert actual_real_share_amount == expected_real_share_amount



if __name__ == '__main__':
    pytest.main()