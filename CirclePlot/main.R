source("CirclePlot.R")


node_names <- read.csv(file="nodeNames.csv", header=FALSE, sep=",")
node_names <- node_names$V1
a <- read.table("matrix.txt", header = FALSE, sep = "")
p <- make_circle_plot(a, node_names, 0.025, 0.25)
