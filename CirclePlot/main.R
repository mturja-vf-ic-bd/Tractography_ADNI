source("CirclePlot.R")

args <- commandArgs(trailingOnly = TRUE)
adj_mat <- args[1]
node_names <- read.csv(file="nodeNames.csv", header=FALSE, sep=",")
node_names <- node_names$V1
a <- read.table(adj_mat, header = FALSE, sep = "")
p <- make_circle_plot(a, node_names, 0, 0.8, adj_mat)
