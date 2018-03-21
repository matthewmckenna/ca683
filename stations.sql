-- some queries to extract the unique stations from the journey dataset
.once _start_stations
SELECT DISTINCT start_station_id FROM journey;

.once _end_stations
SELECT DISTINCT end_station_id FROM journey;
