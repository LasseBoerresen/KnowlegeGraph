"""
You must write an algorithm that calculates some numbers for an ownership structure.

There are a total of 2 ownership structures:

Resights ApS, which is simple and easy to get started with
Casa A/S, which is much more complex, e.g. two companies can own each other or a company can own another company through several subsidiaries


The task essentially involves one company (or person) owning another company - and the share they own is given to us in a range, e.g. 10-15%. That company can then own another company, let's say with 50%. The original company or person, therefore, owns company no. 3 with 10-15% * 50% = 5 to 7.5%.

It might therefore be a good idea to split the range into a lower, middle, and upper value, e.g. for 10-15%, it would be 10%, 12.5%, and 15%.

When we look at a "real" ownership between two companies, we are always interested in knowing how much they own of the company we are focusing on (company with depth = 0, it is also the same company the file is named after).

That is, the file where Resights ApS is in focus, and Mikkel owns 100% of Duif Holding, which owns 33-50% of Resights ApS, the real ownership for Mikkel of Resights should be indicated as 33-50%, as it is Resights that is in focus.

Note that for e.g. Casa A/S, there are companies both below and above Casa A/S itself. All ranges must therefore be readable, how much does the "source" own of the company in focus? Or how much does the company in focus own of the "target" for companies below the company in focus.

I have attached some images (without solution, but with the direct ownership intervals) so you can get a visual overview.

Let me know if there is anything that requires further explanation :-)
"""
from __future__ import annotations

from typing import Callable, Optional

from depth import Depth
from entity import Entity
from share import Share
from share_amount import ShareAmount


class ShareGraphSparseDictImpl:
    def __init__(self) -> None:
        self.__focus: Optional[Entity] = None
        self.__entity_real_share_amount_cache: dict[(Entity, Entity), ShareAmount] = {}
        self.__entity_with_depth_dict: dict[Entity, Depth] = {}
        self.__source_with_shares_dict: dict[Entity, list[Share]] = {}
        self.__target_with_shares_dict: dict[Entity, list[Share]] = {}

    def real_share_amounts(self) -> dict[Entity, ShareAmount]:
        return {
            source: self.real_share_amount_for(source)
            for source in self.__entity_with_depth_dict.keys()}

    def real_share_amount_for(self, query: Entity) -> ShareAmount:
        return self.__real_share_amount_for(query, visits={}).throw_if_not_faction()

    def __real_share_amount_for(self, query: Entity, visits: dict[Entity, int]) -> ShareAmount:
        if query in self.__entity_real_share_amount_cache:
            return self.__entity_real_share_amount_cache[query]

        real_share_amount =  self.__real_share_amount_uncached(query, visits)

        return real_share_amount

    def __real_share_amount_uncached(self, query: Entity, visits: dict[Entity, int]) -> ShareAmount:
        self.visit(query, visits)

        if visits[query] > 1:
            return ShareAmount.from_exact(0.0)

        if query == self.focus:
            return ShareAmount.from_exact(1.0)

        return self.__real_share_amount_multi_directional_for(query, visits)

    def __real_share_amount_multi_directional_for(self, query, visits) -> ShareAmount:
        query_depth = self.__entity_with_depth_dict[query].value
        if query_depth >= 0:
            shares = self.__source_with_shares_dict[query]
            query_selector = lambda share: share.target
        else:
            shares = self.__target_with_shares_dict[query]
            query_selector = lambda share: share.source

        real_share_amount = self.__calculate_real_share_amount_for(shares, query_selector, visits.copy())

        if self.__should_cache(real_share_amount):
            self.__entity_real_share_amount_cache[query] = real_share_amount

        return real_share_amount

    @staticmethod
    def __should_cache(real_share_amount) -> bool:
        return real_share_amount.value.upper.value > 0.0

    def __calculate_real_share_amount_for(
            self,
            shares: list[Share],
            query_selector: Callable[[Share], Entity],
            visits: dict[Entity, int]) -> ShareAmount:

        # Note: Recursive calls
        # Note: Each branching path maintains a different visitor dict. Circularity is per path
        real_share_amounts = [
            share.amount * self.__real_share_amount_for(query_selector(share), visits.copy())
            for share in shares]

        return sum(real_share_amounts, start=ShareAmount.from_exact(0.0))

    @staticmethod
    def visit(source, visits):
        visits[source] = visits[source] + 1 if source in visits else 1

    def __add_shares(self, shares) -> None:
        for share in shares:
            self.__add_share(share)

        self.__set_focus()

    def __set_focus(self):
        self.focus = next(
            key
            for key, depth in self.__entity_with_depth_dict.items()
            if depth.value == 0)

    def __add_share(self, share) -> None:
        self.__add_entities_for(share)

        self.__add_source_for(share)
        self.__add_target_for(share)

    def __add_source_for(self, share):
        if share.source not in self.__source_with_shares_dict:
            self.__source_with_shares_dict[share.source] = []

        self.__source_with_shares_dict[share.source].append(share)

    def __add_target_for(self, share):
        if share.target not in self.__target_with_shares_dict:
            self.__target_with_shares_dict[share.target] = []

        self.__target_with_shares_dict[share.target].append(share)

    def __add_entities_for(self, share):
        self.add_entity(share.source, share.source_depth)
        self.add_entity(share.target, share.target_depth)

    def add_entity(self, entity, entity_depth):
        if self.should_add_entity_depth(entity, entity_depth):
            self.__entity_with_depth_dict[entity] = entity_depth

    def should_add_entity_depth(self, entity, entity_depth):
        return (entity not in self.__entity_with_depth_dict
                or abs(entity_depth.value) < self.__entity_with_depth_dict[entity].value)

    @classmethod
    def create_from(cls, shares: list[Share]) -> ShareGraphSparseDictImpl:
        graph = ShareGraphSparseDictImpl()

        shares = Share.filter_to_active_shares(shares)

        graph.__add_shares(shares)

        return graph