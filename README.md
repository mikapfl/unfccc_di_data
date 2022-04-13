[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4198782.svg)](https://doi.org/10.5281/zenodo.4198782)

Dataset containing all data available from the UNFCCC API at https://di.unfccc.int as of 2021-12-03.

Due to the large size of the full dataset, the dataset is shared on using [datalad](https://www.datalad.org/) and on [zenodo](https://doi.org/10.5281/zenodo.4198782).

To obtain the data using datalad, first clone the repository including metadata:
```shell
$ datalad clone https://github.com/mikapfl/unfccc_di_data.git
```
Then you can fetch the data using datalad:
```shell
$ cd unfccc_di_data
$ datalad get -r .
```
You can learn more about datalad in the [datalad handbook](http://handbook.datalad.org).

References:
All the data included in this dataset is available from the UNFCCC API, which sources the data from:
* GHG inventory data: UNFCCC: Greenhouse Gas Inventory Data, available at https://unfccc.int/process/transparency-and-reporting/greenhouse-gas-data/what-is-greenhouse-gas-data
* Population data: UNSD Demographic Statistics, available at http://data.un.org
* GDP data: The World Bank GDP data, available at https://data.worldbank.org/ and shared by The World Bank under the [CC-BY 4.0 License](https://creativecommons.org/licenses/by/4.0/) and pusuant to their [terms of use](https://data.worldbank.org/summary-terms-of-use).

Included is also a python script `download.py` to download the most recent version of the data from the UNFCCC API, which uses the [unfccc-di-api library](https://pypi.org/project/unfccc-di-api/).

License: the python scripts are provided under the Apache License, Version 2.0.
