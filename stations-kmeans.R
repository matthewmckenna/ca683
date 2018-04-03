#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)

# load libraries ------------------------------------------------------------
library(readr)
library(ggplot2)

if (length(args) == 0) {
    stop("you must supply the data_dir argument", call. = FALSE)
}
# set the input and output data directory
data_dir <- args[1]

# set seed for reproducibility
set.seed(0)

# read data -----------------------------------------------------------------
input_file <- paste(data_dir, "bp.csv", sep = "/")
df <- read_csv(input_file)

# plot and save the unclustered image ---------------------------------------
plt <- ggplot(data = df) +
    geom_point(mapping = aes(x = lon, y = lat, alpha = 0.5), show.legend = FALSE)
output_file <- paste(data_dir, "stations.png", sep = "/")
ggsave(output_file, plot = plt, device = "png", width = 7, height = 4.67)

# columns 3 and 4 are latitude and longitude respectively -------------------
for (k in 5:20) {
    clust <- kmeans(df[, 3:4], centers = k, nstart = 20)
    clust$cluster <- as.factor(clust$cluster)
    plt <- ggplot(data = df) +
        geom_point(mapping = aes(x = lon, y = lat, colour = clust$cluster), show.legend = FALSE)
    output_file <- paste(data_dir, paste("kmeans_k", k, sep = ""), sep = "/")
    # create an image that is 2100 x 1400
    ggsave(paste(output_file, ".png", sep = ""), plot = plt, width = 7, height = 4.67)
}
