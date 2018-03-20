#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)

# load libraries ------------------------------------------------------------
library(readr)
library(lubridate)
library(dplyr)

if (length(args) == 0) {
    stop("you must supply the data_dir argument", call. = FALSE)
}
# set the input and output data directory
data_dir <- args[1]

# set seed for reproducibility
set.seed(0)
num_samples <- 10000

# functions -----------------------------------------------------------------
get_start_month_sample <- function(df, month, n) {
    df[sample(which(df$start_month == month), n), ]
}

get_start_wday_sample <- function(df, wday, n) {
    df[sample(which(df$start_wday == wday), n), ]
}


# read raw data -------------------------------------------------------------
input_file <- paste(data_dir, "journey.csv", sep = "/")
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

# sample from each month and combine into a dataframe -----------------------
datalist = list()

for (i in 1:12) {
   datalist[[i]] <- get_start_month_sample(df, i, num_samples)
}

sampled_df <- bind_rows(datalist)

# save the sampled file -----------------------------------------------------
output_file <- paste(data_dir, "sampled_journey_10k_pm.csv", sep = "/")
write_csv(sampled_df, path = output_file)

