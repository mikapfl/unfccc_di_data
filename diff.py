"""Compute and summarize differences."""

import os
import pandas as pd
import datacompy
import tqdm


dfs = [
    pd.read_parquet(f"data/old/{i}")
    for i in os.listdir("data/old")
    if i.endswith(".parquet")
]
old = pd.concat(dfs)

sort_cols = ["party", "category", "classification", "measure", "gas", "unit", "year", "numberValue", "stringValue"]
old = old.sort_values(
    sort_cols,
    ignore_index=True
)

new = pd.read_parquet("data/all.parquet")

new = new.sort_values(
    sort_cols,
    ignore_index=True
)

join_columns=["party", "category", "classification", "measure", "gas", "year"]

for party in tqdm.tqdm(new["party"].unique()):
    o = old[old["party"] == party].reset_index(drop=True)
    n = new[new["party"] == party].reset_index(drop=True)
    if o.equals(n):
        continue
    if len(o) == len(n):
        diff = o.compare(n)
        if diff.empty:
            continue

    print(f"{party} has differences, generating diff/{party}.html")

    o = n.set_index(join_columns, drop=True)
    n = o.set_index(join_columns, drop=True)

    comp = datacompy.Compare(o, n, on_index=True,
                             df1_name="old", df2_name="new", cast_column_names_lower=False)
    comp.report(html_file=f"diff/{party}.html")
    with open(f"diff/{party}.html", 'a') as fd:
        fd.write("<h2>Only in old</h2>\n")
        comp.df1_unq_rows.sort_values(sort_cols).to_html(fd)
        fd.write("<h2>Only in new</h2>\n")
        comp.df2_unq_rows.sort_values(sort_cols).to_html(fd)
        fd.write("<h2>Changed</h2>\n")
        am = comp.all_mismatch()
        am.sort_values(list(am.columns)).to_html(fd)
