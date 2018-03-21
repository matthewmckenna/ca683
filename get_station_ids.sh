#!/bin/bash
# extract the unique station ids from `journey.db` and write to files

# directory containing `journey.db`
data_dir=$1

sqlite3 $data_dir/journey.db <stations.sql

# sort the station ids numerically
sort -n _start_stations >$data_dir/start_station_ids.txt
sort -n _end_stations >$data_dir/end_station_ids.txt

# remove the intermediate files
rm _start_stations _end_stations
