# How to create a new release
## 1. download and publish new data
Go to https://github.com/mikapfl/unfccc_di_data/actions/workflows/download.yaml and
trigger a new run of the "download" workflow. This will download the latest data from
the UNFCCC and add it to the data package on gin.hemio.de

The workflow takes about 10 minutes to run.

## 2. pull changed data, examine changes

In a terminal in your local checkout of the unfccc_di_data package, run:

```shell
datalad update -s ginhemio --how merge
datalad update
git pull
```

to pull all changes.

If you want to compare differences, checkout the base you want to compare against,
move the CSVs from it to a temporary folder called `old`, then checkout the latest
state again and copy the CSVs to a temporary folder called `new`.
Then run (in fish):

```fish
for i in old/*.csv; echo $i; csvdiff --ignore-columns 0 -p 1,2,3,4,5,7 -o word-diff $i  new/$(basename $i) > diff_$(basename $i); end
```

you need https://github.com/aswinkarthik/csvdiff for that. Afterwards, you can check
the `diff_{country}.csv` files for changes.

## 3. release a new version of the data package

If you are happy, start making a new version on zenodo and get a pre-reserved doi.
Put the new doi and new citation info into datacite.yml and README.md

Then run:

```shell
datalad save
datalad push
datalad push --to origin
datalad push --to ginhemio --data anything
datalad export-archive -t zip "data-$(date --iso).zip"
zip parquet-only.zip data/annexI/*.parquet data/non-annexI/*.parquet
```

upload the new data (consisting of the data-{date}.zip and parquet-only.zip files) to
zenodo.

## 4. start using the new version

To use the new version of the data package from other places, you should release a new
version of the `unfccc_di_api` package, in particular update the default values for
the `ZenodoReader` class in the file `unfccc_di_api.py`.
