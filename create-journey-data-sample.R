#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)

# load libraries ------------------------------------------------------------
library(readr)
library(dplyr)

if (length(args) != 2) {
    stop("you must supply the input and output filenames", call. = FALSE)
}
# set the input and output data directory
input_file <- args[1]
output_file <- args[2]

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

# read input data -----------------------------------------------------------
df <- read_csv(input_file)

# sample from each month and combine into a dataframe -----------------------
datalist = list()

for (i in 1:12) {
   datalist[[i]] <- get_start_month_sample(df, i, num_samples)
}

sampled_df <- bind_rows(datalist)

# save the sampled file -----------------------------------------------------
write_csv(sampled_df, path = output_file)
