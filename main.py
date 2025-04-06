from pathlib import Path

from share_graph import ShareGraphSparseDictImpl
from shares_file_reader import SharesFileReader


def main():
    filepath = Path('data/CasaAS.json')
    shares = SharesFileReader.read_shares_from(filepath)
    focus_entity = SharesFileReader.read_focus_entity_from(filepath)

    sg = ShareGraphSparseDictImpl.create_from(shares)
    real_shares_dict = sg.real_shares_amounts_in(focus_entity)

    for source, real_share in real_shares_dict.items():
        print(f"{real_share}: {source}")

    # TODO: be careful when calculating mean share.. Could be different than just  min+max/2,
    #  but maybe all averages should be aggregated.


if __name__ == "__main__":
    main()