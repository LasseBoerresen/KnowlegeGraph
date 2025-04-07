# tests/test_share_graph.py
from collections import namedtuple

import pytest

from depth import Depth
from entity import Entity
from entity_id import EntityId
from entity_name import EntityName
from ratio_range import RatioRange
from share import Share
from share_amount import ShareAmount
from share_graph import ShareGraph


from typing import NamedTuple


class TestInput(NamedTuple):
    shares: list[Share]
    entity_queried: Entity
    expected_real_share_amount: ShareAmount


class TestShareGraph:

    @staticmethod
    def create_test_entity(entity_id: int):
        return Entity(id=EntityId(entity_id), name=EntityName(f"{entity_id}"))

    e0 = create_test_entity(0)
    e1 = create_test_entity(1)
    e2 = create_test_entity(2)
    e3 = create_test_entity(3)
    e_1 = create_test_entity(-1)
    e_2 = create_test_entity(-2)

    @pytest.mark.parametrize(
        "shares, entity_queried, expected_real_share_amount",
        [
            # Given: Single 1.0 share
            # Then: returns that share directly as 1.0
            TestInput(
                shares=[Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0))],
                entity_queried=e1,
                expected_real_share_amount=ShareAmount.from_exact(1.0)),

            # Given: Single 0.5 share
            # Then:  return that share directly as 0.5
            TestInput(
                shares=[Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5))],
                entity_queried=e1,
                expected_real_share_amount=ShareAmount.from_exact(0.5)),

            # Given: two 0.5 shares in serial
            # Then:  then compounds both two to 0.25
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5))],
                entity_queried=e2,
                expected_real_share_amount=ShareAmount.from_exact(0.25)),

            # Given: three 0.5 shares in serial
            # Then:  compounds all 3 to 0.125
            TestInput(
                shares=[
                    Share(source=e3, source_depth=Depth(3), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5))],
                entity_queried=e3,
                expected_real_share_amount=ShareAmount.from_exact(0.125)),

            # Given two serial share amounts with ranges
            # Then:  returns lower compounded with lower, and upper compounded with upper.
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_range(0.5,1.0)),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_range(0.5, 1.0))],
                entity_queried=e2,
                expected_real_share_amount=ShareAmount.from_range(0.25, 1.0)),

            # Given: three 0.5 shares, 1 direct and 2 in series to focus
            # Then:  0.75
            TestInput(
                shares=[
                    Share(source=e3, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e3, source_depth=Depth(2), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5))],
                entity_queried=e3,
                expected_real_share_amount=ShareAmount.from_exact(0.25+0.125)),

            # Given: single negative_depth target with 0.5 shares
            # Then:  0.5
            TestInput(
                shares=[Share(source=e0, source_depth=Depth(0), target=e_1, target_depth=Depth(-1), amount=ShareAmount.from_exact(0.5))],
                entity_queried=e_1,
                expected_real_share_amount=ShareAmount.from_exact(0.50)),

            # Given: two negative_depth target with 0.5 shares
            # Then:  0.25
            TestInput(
                shares=[
                    Share(source=e0, source_depth=Depth(0), target=e_1, target_depth=Depth(-1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e_1, source_depth=Depth(-1), target=e_2, target_depth=Depth(-2), amount=ShareAmount.from_exact(0.5))],
                entity_queried=e_2,
                expected_real_share_amount=ShareAmount.from_exact(0.25)),

            # Given: three shares, where last is circular and query for depth 2
            # Then:  ignores circular path and returns 0.5
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0)),
                    Share(source=e1, source_depth=Depth(3), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.1))],
                entity_queried=e2,
                expected_real_share_amount=ShareAmount.from_exact(0.5)),

            # Given: three shares, where last is circular and query for depth 1
            # Then:  ignores circular path and returns 1.0
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0)),
                    Share(source=e1, source_depth=Depth(3), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.1))],
                entity_queried=e1,
                expected_real_share_amount=ShareAmount.from_exact(1.0)),

            # Given: four shares, where in two level circular path and query for depth 2
            # Then:  ignores circular path and returns direct path 0.5*1.0 = 0.5
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0)),
                    Share(source=e1, source_depth=Depth(4), target=e3, target_depth=Depth(3), amount=ShareAmount.from_exact(0.1)),
                    Share(source=e3, source_depth=Depth(3), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.1))],
                entity_queried=e2,
                expected_real_share_amount=ShareAmount.from_exact(0.5)),

            # Given: three shares, where last is circular and query for depth -2
            # Then:  ignores circular path and returns 0.25
            TestInput(
                shares=[
                    Share(source=e0, source_depth=Depth(0), target=e_1, target_depth=Depth(-1), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e_1, source_depth=Depth(-1), target=e_2, target_depth=Depth(-2), amount=ShareAmount.from_exact(0.5)),
                    Share(source=e_2, source_depth=Depth(-3), target=e_2, target_depth=Depth(-1), amount=ShareAmount.from_exact(0.1))],
                entity_queried=e_2,
                expected_real_share_amount=ShareAmount.from_exact(0.25)),



            # TODO test that lower and upper bounds are calculated correctly.


        ])
    def test_given_shares_and_focus_and_queried_entity__when_get_real_share__then_returns_expected(
            self,
            shares: list[Share],
            entity_queried: Entity,
            expected_real_share_amount: ShareAmount):

        # Given
        graph = ShareGraph.create_from(shares)

        # When
        actual_real_share_amount = graph.real_share_amount_for(query=entity_queried)

        # Then
        assert actual_real_share_amount == expected_real_share_amount



if __name__ == '__main__':
    pytest.main()