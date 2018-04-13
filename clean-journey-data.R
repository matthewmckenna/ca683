#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)

# load libraries ------------------------------------------------------------
library(readr)
library(lubridate)

if (length(args) != 2) {
    stop("you must supply the input and output filenames", call. = FALSE)
}
# set the input and output data directory
input_file <- args[1]
output_file <- args[2]

# read raw data -------------------------------------------------------------
df <- read_csv(input_file)
# replace spaces in column names with periods
colnames(df) <- make.names(colnames(df), unique = TRUE)

# create new columns --------------------------------------------------------
# format the start timestamp
df$start_ts <- dmy_hm(df$Start.Date, tz = "Europe/London")
df$start_month <- month(df$start_ts)
# add a column for the day of the week - 1 = Monday, .., 7 = Sunday
df$start_wday <- wday(df$start_ts, week_start = 1)
df$start_hour <- hour(df$start_ts)
# add a column to signify whether or not the bike was hired on a weekday
df$start_isweekday <- as.numeric(df$start_wday < 6)

# format the end timestamp
df$end_ts <- dmy_hm(df$End.Date, tz = "Europe/London")
df$end_month <- month(df$end_ts)
# add a column for the day of the week - 1 = Monday, .., 7 = Sunday
df$end_wday <- wday(df$end_ts, week_start = 1)
df$end_hour <- hour(df$end_ts)
# add a column to signify whether or not the bike was hired on a weekday
df$end_isweekday <- as.numeric(df$end_wday < 6)

# remove some columns ------------------------------------------------------
df$Start.Date <- NULL
df$End.Date <- NULL
df$StartStation.Name <- NULL
df$EndStation.Name <- NULL

# update the column names ----------------------------------------------------
colnames(df) <- c(
  "rental_id",
  "duration",
  "bike_id",
  "end_station_id",
  "start_station_id",
  colnames(df)[6:15]
)

# save the cleaned file ------------------------------------------------------
write_csv(df, path = output_file)
