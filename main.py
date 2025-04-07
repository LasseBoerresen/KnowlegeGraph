from pathlib import Path
from share_graph import ShareGraphSparseDictImpl
from shares_file_reader import SharesFileReader


def main():
    filepath = Path('data/ResightsApS.json')
    share_dtos = SharesFileReader.read_shares_from(filepath)

    shares = [dto.to_domain() for dto in share_dtos]
    share_graph = ShareGraphSparseDictImpl.create_from(shares)
    entity_and_real_share_amount_dict = share_graph.real_share_amounts()

    for source, real_share in entity_and_real_share_amount_dict.items():
        print(f"{real_share.to_percentage_str()}: {source}")

    SharesFileReader.write_real_shares_to(filepath, entity_and_real_share_amount_dict)

if __name__ == "__main__":
    main()