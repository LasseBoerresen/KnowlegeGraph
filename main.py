from pathlib import Path

from share_graph import ShareGraphSparseDictImpl
from shares_file_reader import SharesFileReader


def main():
    filepath = Path('data/CasaAS.json')
    shares = SharesFileReader.read_shares_from(filepath)

    share_graph = ShareGraphSparseDictImpl.create_from(shares)
    real_share_amounts_dict = share_graph.real_share_amounts()

    for source, real_share in real_share_amounts_dict.items():
        print(f"{real_share}: {source}")

    # TODO: be careful when calculating mean share.. Could be different than just  min+max/2,
    #  but maybe all averages should be aggregated.


if __name__ == "__main__":
    main()