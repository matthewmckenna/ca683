#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)

# load libraries ------------------------------------------------------------
library(readr)
library(zoo)

if (length(args) != 3) {
  stop("you must supply the journey dataset, weather dataset and output filename",
       call. = FALSE)
}
# set the input and output data directory
journey_file <- args[1]
weather_file <- args[2]
output_file <- args[3]

# read journey data ---------------------------------------------------------
# journey_filename <- paste(data_dir, "journey_clean01.csv", sep = "/")
journey <- read_csv(journey_file)

# read weather data ---------------------------------------------------------
# weather_filename <- paste(data_dir, "weather_02.csv", sep = "/")
weather <- read_csv(weather_file)

# forward-fill the missing condition observatiosn ---------------------------
weather <- na.locf(weather)

# convert the character field to a datetime field ---------------------------
weather$datetime <- as.POSIXct(weather$datetime)

# merge the dataframes -------------------------------------------------------
df <-
  cbind(journey, weather[sapply(journey$start_ts, function(x)
    which.min(abs(x - weather$datetime))), c(
      "temperature",
      "humidity",
      "wind_speed",
      "condition",
      "rain",
      "snow",
      "hail",
      "fog",
      "thunder"
    )])

# save the merged file -------------------------------------------------------
# output_file <- paste(data_dir, "journey_weather_merge.csv", sep = "/")
write_csv(df, path = output_file)
