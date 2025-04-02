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

class KnowledgeGraph:
    def __init__(self, company_name, ownership_structure):
        self.company_name = company_name
        self.ownership_structure = ownership_structure