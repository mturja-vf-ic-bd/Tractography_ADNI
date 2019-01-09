source("CirclePlot.R")


node_names <- read.csv(file="nodeNames.csv", header=FALSE, sep=",")
node_names <- node_names$V1
a <- read.table("S186178_fdt_network_matrix_row_normalized", header = FALSE, sep = "")
p <- make_circle_plot(a, node_names, 0.025, 0.25)
