"""Download the data for all countries from the """
import pandas as pd
import tqdm
import os
import pathlib

from unfccc_di_api import UNFCCCApiReader

ROOT_DIR = pathlib.Path(os.path.abspath(os.curdir))


def main():
    r = UNFCCCApiReader()
    dfs = []
    for party in tqdm.tqdm(r.parties["code"], desc="parties"):
        df = r.query(party_code=party, progress=False)

        annexI = party in r.annex_one_reader.parties["code"].values
        subdir = "annexI" if annexI else "non-annexI"
        directory = ROOT_DIR / "data" / subdir
        directory.mkdir(parents=True, exist_ok=True)
        # CSV compressed with gzip is a very widely used standard
        # pass mtime=0 explicitly so that the creation time is not embedded in the
        # produced gzip file, which means that the gzip file doesn't change if the
        # contents haven't changed.
        df.to_csv(
            directory / f"{party}.csv.gz",
            compression={"method": 'gzip', "mtime": 0}
        )
        dfs.append(df)

    # Save data for all parties into one big file for easy distribution.
    # parquet with zstd compression is a very efficient binary format
    # unfortunately, it embeds the used software versions in the metadata so
    # generally, the parquet file can change even if the contents haven't changed.
    # We disable index and statistics which we don't use.
    df_all = pd.concat(dfs)
    df_all.to_parquet(
        ROOT_DIR / "data" / "all.parquet",
        engine="fastparquet",
        compression="zstd",
        index=False,
        stats=False
    )


if __name__ == "__main__":
    main()
