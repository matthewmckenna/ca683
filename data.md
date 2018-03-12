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

## Weather Data

Hourly weather data was retrieved from the Weather Underground API. The data was
downloaded in JSON format, with one file per day. There were 369 JSON files
downloaded from Weather Underground, and these files are available in the
following [archive](https://drive.google.com/open?id=1RDIjwpvLRi8Wr7F2VNhtd08WcHm8J9_n).
The archive is approximately 1 MB uncompressed.

These files were also merged and are provided below in CSV and SQLite format:

* CSV file: [weather.csv](https://drive.google.com/open?id=1e1U3Mcowvsnp6-rZCODJ-PVZsda0xihA) [873 KB]
* SQLite file: [weather.db](https://drive.google.com/open?id=1ptnDBUt3u3Q7CYrBd4TvU8bIr1pASdKw) [872 KB]


## Bikepoints

Data relating to the stations (or "bikepoints") for London cycles was retrieved
using the Transport for London Unified API.

* Original JSON file: [bikepoints.json](https://drive.google.com/open?id=1_iKp8HZWQiWJPZius9ZcGVynM-Q1h2U9) [1.8 MB]
* Preprocessed CSV file: [bikepoints.csv](https://drive.google.com/open?id=1IRawKHUsyEfPtUG_gQzpnF4kTeM79pMo) [52 KB]
