# How to create a new release

New data is automatically downloaded and added to the dataset every month. While this
is useful for data archeology in the datalad dataset, an official release on
zenodo is needed so you can cite the data and third parties can easily re-use the data.
We therefore aim to make a new release whenever relevant changes happened or at least
twice a year.

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
move the `all.parquet` file from it to a temporary new name, then checkout the latest
state again.
Then you can point the `diff.py` script at the files you just checked out and run it
to generate HTML files which show the differences between the old and the new state.
Note that if there are no differences, no HTML files are generated.

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
```

upload the new data (consisting of the data-{date}.zip and data/all.parquet files) to
zenodo.

## 4. start using the new version

To use the new version of the data package from other places, you should release a new
version of the `unfccc_di_api` package, in particular update the default values for
the `ZenodoReader` class in the file `unfccc_di_api.py`.
