# Data

Data for this project are stored on Google Drive.

## Journey Data

Cycle hire data are published by Transport for London. The data are provided
in CSV files, each containing one week worth of data. These files are available
in a *tarball* (.tar.gz) [here](https://drive.google.com/open?id=1GZtYqej5tEDnQj3g5qB_fmy_k76YFseC).
The archive is approximately 1.2 GB uncompressed.

The data from the 52 CSV files were merged and are provided below in CSV and
SQLite format:

* Gzipped CSV file: [journey.csv.gz](https://drive.google.com/open?id=1HSnVe74BsBfvsX1B2tyv60O9O-lAaJV-) [242 MB]
* Gzipped SQLite file: [journey.db.gz](https://drive.google.com/open?id=1hTPquBMo_sp0VZQAWh5shmFNNjDAjs_o) [327 MB]

A stratified random sample of the journey dataset was created to speed up the
initial analysis. The main criterion was that there be an equal number of
observations from each month of the year. The number of observations per month
was chosen to be 10,000, resulting in a dataset of 120,000 total observations.
This data is available in CSV format and is 10 MB uncompressed.

* Gzipped CSV file: [sampled_journey_10k_pm.csv.gz](https://drive.google.com/file/d/1CPpFetJcbO2P0H5gyxMuPt3jyPyo0aWu/view?usp=sharing) [3 MB]

## Weather Data

Hourly weather data was retrieved from the Weather Underground API. The data was
downloaded in JSON format, with one file per day. There were 369 JSON files
downloaded from Weather Underground, and these files are available in the
following [archive](https://drive.google.com/open?id=1RDIjwpvLRi8Wr7F2VNhtd08WcHm8J9_n).
The archive is approximately 1 MB uncompressed.

These files were also merged and are provided below in CSV and SQLite format:

* CSV file: [weather.csv](https://drive.google.com/open?id=1e1U3Mcowvsnp6-rZCODJ-PVZsda0xihA) [873 KB]
* SQLite file: [weather.db](https://drive.google.com/open?id=1ptnDBUt3u3Q7CYrBd4TvU8bIr1pASdKw) [872 KB]

The weather dataset has been updated with the following changes:

1. `date` and `time` fields have been merged into a single `datetime` field.
2. `precipitation` field has been dropped.
3. `condition` field has been grouped, and reduced from `25` to `5` cateogries.

* CSV file: [weather_02.csv](https://drive.google.com/open?id=1YVUpEovKr7Of05koUy1vrVPPzToHl5_T) [753 KB]

For a list of the `condition` field groupings please see the project notes document.

## Bikepoints

Data relating to the stations (or "bikepoints") for London cycles was retrieved
using the Transport for London Unified API.

* Original JSON file: [bikepoints.json](https://drive.google.com/open?id=1_iKp8HZWQiWJPZius9ZcGVynM-Q1h2U9) [1.8 MB]
* Preprocessed CSV file: [bikepoints.csv](https://drive.google.com/open?id=1IRawKHUsyEfPtUG_gQzpnF4kTeM79pMo) [52 KB]

An updated bikpoints dataset was retrieved which contained previously missing
data for stations `47` and `411`. This dataset is missing data for station `527`
which was previously available.

* Updated JSON file: [bikepoints2.json](https://drive.google.com/open?id=1ApzPZmw8FEhB9GEO8Zbm4MCGI37mW4mi) [2 MB]

A superset of the two bikepoints JSON files is available below, with data for
`784` stations.

* CSV superset of stations: [bp.csv](https://drive.google.com/open?id=1v8IAS5724AaLi1XirWD-r8tJds44qPaS) [52 KB]
