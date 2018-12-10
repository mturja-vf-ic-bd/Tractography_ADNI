# Libraries
library(ggraph)
library(igraph)
library(tidyverse)
library(RColorBrewer)
library(rlist)
library(RColorBrewer)
library(wesanderson)

make_circle_plot <- function(my_mat, node_names, lower_edge, upper_edge, my_title = NULL, my_lims = NULL) {
  	# create a data frame giving the hierarchical structure of the nodes
  	nregions <- 148
  	nclass <- 12
  	lobes <- c("l_Frontal", "l_Limbic", "l_Insula", "l_Parietal", "l_Temporal", "l_Occipital", "r_Occipital", "r_Temporal", "r_Parietal", "r_Insula", "r_Limbic", "r_Frontal")
  	d1 <- data.frame(from="origin", to=lobes)
 	d1$to <- as.character(d1$to)
 	print(d1)
 	names(d1) <- c("from", "to")
  	d2=data.frame(from=c(rep(d1$to[1], 22), rep(d1$to[2], 8), rep(d1$to[3], 6), rep(d1$to[4], 12), rep(d1$to[5], 12), rep(d1$to[6], 14),
                       rep(d1$to[7], 14), rep(d1$to[8], 12), rep(d1$to[9], 12), rep(d1$to[10], 6), rep(d1$to[11], 8), rep(d1$to[12], 22)), to=node_names)
	names(d2) <- c("from", "to")
	edges <- rbind(d1, d2)
	d1$to <- as.factor(d1$to)
	# create a dataframe with connection between leaves 
	node_indices <- expand.grid(Cols = 1:nregions, Rows = 1:nregions)
	connect <- data.frame(from = node_names[node_indices$Rows], to = node_names[node_indices$Cols], value = as.vector(t(my_mat)))
	connect <- connect[which(connect$value > lower_edge &  connect$value < upper_edge),]

	# create a vertices data.frame. One line per object of our hierarchy
	vertices <- data.frame(name = unique(c(as.character(edges$from), as.character(edges$to)))) 
	# Let's add a column with the group of each name. It will be useful later to color points
	vertices$group <- edges$from[ match( vertices$name, edges$to ) ]

	#Let's add information concerning the label we are going to add: angle, horizontal adjustement and potential flip
	#calculate the ANGLE of the labels
	vertices$id <- NA
	myleaves <- which(is.na( match(vertices$name, edges$from) ))
	nleaves <- length(myleaves)
	vertices$id[ myleaves ] <- seq(1:nleaves)
	vertices$angle <- 90 - 360 * vertices$id / nleaves

	# calculate the alignment of labels: right or left
	# If I am on the left part of the plot, my labels have currently an angle < -90
	vertices$hjust <- ifelse(vertices$angle < -90, 1, 0)

	# flip angle BY to make them readable
	vertices$angle <- ifelse(vertices$angle < -90, vertices$angle+180, vertices$angle)

	# Create a graph object
	mygraph <- graph_from_data_frame( edges, vertices=vertices )

	# The connection object must refer to the ids of the leaves:
	from <- match( connect$from, vertices$name)
	to <- match( connect$to, vertices$name)

	# Basic usual argument
	png("circle_plot.png", height = 1080, width = 1080)
	p <- ggraph(mygraph, layout = 'dendrogram', circular = TRUE) + 
	geom_conn_bundle(data = get_con(from = from, to = to, value=connect$value), aes(colour=value, alpha=value, width=value), tension=0.7) +
	scale_edge_colour_distiller(type = "div" , palette = "Spectral", limits = c(lower_edge, upper_edge)) +
	geom_node_text(aes(x=x*1.02, y=y*1.02, filter = leaf, label=name, angle = angle, hjust=hjust), size=5, alpha=1) + 
	theme_void() +
  	expand_limits(x = c(-1.3, 1.3), y = c(-1.3, 1.3)) +
	geom_node_point(aes(filter = leaf, x = x, y = y, colour=group), size=3)

	if (!is.null(my_title)) {
		p <- p + labs(title = my_title)
	}
	print(p)
	dev.off()
	return(p)
}