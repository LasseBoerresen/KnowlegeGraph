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

from entity import Entity
from share import Share
from share_amount import ShareAmount


class ShareGraphSparseDictImpl:
    def __init__(self) -> None:
        self.__source_with_shares_dict: dict[Entity, list[Share]] = {}
        self.__source_real_share_amount_cache: dict[(Entity, Entity), ShareAmount] = {}

        # TODO keep dict of already computed real shares. Think dynamic programming. We look here first.
        # TODO:

    def real_share_amounts_for(self, source: Entity, focus: Entity) -> ShareAmount:
        return self.__real_share_amounts_for(source, focus, visits={})

    def __real_share_amounts_for(self, source: Entity, focus: Entity, visits: dict[Entity, int]) -> ShareAmount:
        self.visit(source, visits)

        if visits[source] > 1:
            # Ignore contributions from
            return ShareAmount.from_exact(0.0)

        # Handle when source is the entity in focus, then we would never stop. I.e. when the source is upstream
        if source == focus:
            return ShareAmount.from_exact(1.0)

        # Note: Recursive calls
        real_share_amounts = [
            share.amount * self.__real_share_amounts_for(share.target, focus, visits)
            for share in (self.__source_with_shares_dict[source])]

        return sum(real_share_amounts, start=ShareAmount.from_exact(0.0))

    def visit(self, source, visits):
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

    def compute_real_shares_in(self, focus: Entity) -> dict[Entity, ShareAmount]:
        # TODO Do montecarlo simulation of simple circular calculation to determine if the true ownership changes over iterations.
        # TODO: Maybe detect circular shares if target is lower depth than source
        return {
            source: self.real_share_amounts_for(source, focus)
            for source in self.__source_with_shares_dict.keys()}

    def add_shares(self, shares) -> None:
        for share in shares:
            self.add_share(share)

    def add_share(self, share) -> None:
        if share.source not in self.__source_with_shares_dict:
            self.__source_with_shares_dict[share.source] = []

        self.__source_with_shares_dict[share.source].append(share)

    @classmethod
    def create_from(cls, shares: list[Share]) -> ShareGraphSparseDictImpl:
        graph = ShareGraphSparseDictImpl()

        # TODO: Ask about how to interpret inactive edges. You don't show them in your image
        shares = Share.filter_to_active_shares(shares)

        graph.add_shares(shares)

        return graph