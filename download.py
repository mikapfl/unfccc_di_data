import tqdm
import os
import pathlib

from unfccc_di_api import UNFCCCApiReader

ROOT_DIR = pathlib.Path(os.path.abspath(os.curdir))  # This is your Project Root


def main():
    r = UNFCCCApiReader()
    for party in tqdm.tqdm(r.parties["code"], desc="parties"):
        if party != "AUS":
            continue
        df = r.query(party_code=party, progress=False)

        annexI = party in r.annex_one_reader.parties["code"].values
        subdir = "annexI" if annexI else "non-annexI"
        directory = ROOT_DIR / "data" / subdir
        directory.mkdir(parents=True, exist_ok=True)
        df.to_csv(directory / f"{party}.csv.gz", compression="gzip")
        df.to_parquet(directory / f"{party}.parquet", compression="brotli")


if __name__ == "__main__":
    main()
