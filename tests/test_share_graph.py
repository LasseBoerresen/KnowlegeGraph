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
    e3 = create_test_entity(3)
    e_1 = create_test_entity(-1)
    e_2 = create_test_entity(-2)

    @pytest.mark.parametrize(
        "shares, entity_queried, entity_in_focus, expected_real_share_amount",
        [
            # Single 1.0 share
            # Then: 1.0
            TestInput(
                shares=[Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0), active=True)],
                entity_queried=e1,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(1.0)),

            # Given: Single 0.5 share
            # Then:  0.5
            TestInput(
                shares=[Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e1,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.5)),

            # Given: two 0.5 shares in serial
            # Then:  0.25
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e2,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.25)),

            # Given: three 0.5 shares in serial
            # Then:  0.125
            TestInput(
                shares=[
                    Share(source=e3, source_depth=Depth(3), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e3,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.125)),

            # Given: three 0.5 shares, 1 direct and 2 in series to focus
            # Then:  0.75
            TestInput(
                shares=[
                    Share(source=e3, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e3, source_depth=Depth(2), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e3,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.25+0.125)),

            # Given: single negative_depth target with 0.5 shares
            # Then:  0.5
            TestInput(
                shares=[Share(source=e0, source_depth=Depth(1), target=e_1, target_depth=Depth(-1), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e_1,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.50)),

            # Given: two negative_depth target with 0.5 shares
            # Then:  0.25
            TestInput(
                shares=[
                    Share(source=e0, source_depth=Depth(0), target=e_1, target_depth=Depth(-1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e_1, source_depth=Depth(-1), target=e_2, target_depth=Depth(-2), amount=ShareAmount.from_exact(0.5), active=True)],
                entity_queried=e_2,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.25)),

            # Given: three 0.5 shares in serial
            # Then:  0.125
            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.1), active=True)],
                entity_queried=e2,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(0.5)),

            TestInput(
                shares=[
                    Share(source=e2, source_depth=Depth(2), target=e1, target_depth=Depth(1), amount=ShareAmount.from_exact(0.5), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e0, target_depth=Depth(0), amount=ShareAmount.from_exact(1.0), active=True),
                    Share(source=e1, source_depth=Depth(1), target=e2, target_depth=Depth(2), amount=ShareAmount.from_exact(0.1), active=True)],
                entity_queried=e1,
                entity_in_focus=e0,
                expected_real_share_amount=ShareAmount.from_exact(1.0)),


            # TODO test case for forked negative depth query
            # TODO test with circular negative branching path
            # TODO Setup test graph statically, then simply query it in the test cases. Much less setup. Probably as swapable test fixtures.
            # TODO test that lower and upper bounds are calculated correctly.
            # TODO test calculations of average.. through a complicated graph.
            # TODO test other share values than 0.5.

        ])
    def test_given_shares_and_focus_and_queried_entity__when_get_real_share__then_returns_expected(
            self,
            shares: list[Share],
            entity_queried: Entity,
            entity_in_focus: Entity,
            expected_real_share_amount: ShareAmount):

        # Given
        graph = ShareGraphSparseDictImpl.create_from(shares, max_cycle_iterations=2)

        # When
        actual_real_share_amount = graph.real_share_amount_for(query=entity_queried, focus=entity_in_focus)

        # Then
        assert actual_real_share_amount == expected_real_share_amount



if __name__ == '__main__':
    pytest.main()