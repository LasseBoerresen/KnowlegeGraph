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

from typing import Callable

from depth import Depth
from entity import Entity
from share import Share
from share_amount import ShareAmount


class ShareGraphSparseDictImpl:
    def __init__(self) -> None:
        ## TODO actually use the cache
        self.__entity_real_share_amount_cache: dict[(Entity, Entity), ShareAmount] = {}
        self.__entity_with_depth_dict: dict[Entity, Depth] = {}
        self.__source_with_shares_dict: dict[Entity, list[Share]] = {}
        self.__target_with_shares_dict: dict[Entity, list[Share]] = {}

    def real_shares_amounts_in(self, focus: Entity) -> dict[Entity, ShareAmount]:
        # TODO Do montecarlo simulation of simple circular calculation to determine if the true ownership changes over iterations.
        return {
            source: self.real_share_amount_for(source, focus)
            for source in self.__entity_with_depth_dict.keys()}


    def real_share_amount_for(self, query: Entity, focus: Entity) -> ShareAmount:
        return self.__real_share_amount_for(query, focus, visits={})

    def __real_share_amount_for(self, query: Entity, focus: Entity, visits: dict[Entity, int]) -> ShareAmount:
        self.visit(query, visits)

        if visits[query] > 1: # 10
            raise Exception(f"Cycle detected at source: {query}")
            # return ShareAmount.from_exact(1.0)

        if query == focus:
            return ShareAmount.from_exact(1.0)

        return self.__real_share_amount_multi_directional(query, focus, visits)


    def __real_share_amount_multi_directional(self, query, focus, visits) -> ShareAmount:
        query_depth = self.__entity_with_depth_dict[query].value
        if query_depth >= 0:
            shares = self.__source_with_shares_dict[query]
            query_selector = lambda share: share.target
        else:
            shares = self.__target_with_shares_dict[query]
            query_selector = lambda share: share.source

        return self.__calculate_real_share_amount_for(shares, query_selector, focus, visits.copy())

    def __calculate_real_share_amount_for(
            self,
            shares: list[Share],
            query_selector: Callable[[Share], Entity],
            focus: Entity,
            visits: dict[Entity, int]) -> ShareAmount:

        # Note: Recursive calls
        # Note: Each branching path maintains a different visitor dict. Circularity is per path
        real_share_amounts = [
            share.amount * self.__real_share_amount_for(query_selector(share), focus, visits.copy())
            for share in shares]

        return sum(real_share_amounts, start=ShareAmount.from_exact(0.0))

    @staticmethod
    def visit(source, visits):
        visits[source] = visits[source] + 1 if source in visits else 1

    # def __real_share_amounts_for(self, source: Entity, focus: Entity, visits: dict[Entity, int]) -> ShareAmount:
    #     visits[source] += 1
    #
    #     if (source, focus) in self.__source_real_share_amount_cache:
    #         return self.__source_real_share_amount_cache[(source, focus)]
    #
    #     real_share_amount =  self.__real_share_amount_uncached(focus, source, visits)
    #
    #     self.__source_real_share_amount_cache[(source, focus)] = real_share_amount
    #
    #     return real_share_amount
    #
    # def __real_share_amount_uncached(self, focus, source, visits: dict[Entity, int]):
    #     # Handle when source is the entity in focus, then we would never stop. I.e. when the source is upstream
    #     if source == focus:
    #         return ShareAmount.from_exact(1.0)
    #
    #     # Note: Recursive calls
    #     real_share_amounts = [
    #         share.amount * self.real_share_amounts_for(share.target, focus)
    #         for share in (self.__source_with_shares_dict[source])]
    #
    #     return sum(real_share_amounts, start=ShareAmount.from_exact(0.0))

    def add_shares(self, shares) -> None:
        for share in shares:
            self.add_share(share)

    def add_share(self, share) -> None:
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
        self.__entity_with_depth_dict[share.source] = share.source_depth
        self.__entity_with_depth_dict[share.target] = share.target_depth

    @classmethod
    def create_from(cls, shares: list[Share]) -> ShareGraphSparseDictImpl:
        graph = ShareGraphSparseDictImpl()

        # TODO: Ask about how to interpret inactive edges. You don't show them in your image
        shares = Share.filter_to_active_shares(shares)

        graph.add_shares(shares)

        return graph