#r script to parse the blast output from a run, and make some visualizations out of it
#For the interactive graphs, I couldn't get the self_contained option working on the server, that means it outputs the html graph and a folder of supporting files, unfortunately to view the graphs on your computer, you have to transfer both the hmtl graphs and these files to get the graphs working. 
library(ggplot2) 
library(htmlwidgets)
library("dplyr", lib="/home/tgd13003/R/x86_64-pc-linux-gnu-library/3.3")
library("plotly", lib="/home/tgd13003/R/x86_64-pc-linux-gnu-library/3.3")
#ggplot and plotly for visualization. dplyr for data wrangling. htmlwidgets to save the interactive plots
#test yo
blast <- read.table("blast.txt", sep="\t")
colnames(blast) <- c("HE", "evalue", "bitscore", "qstart", "qend", "qframe")
#read in the result from the blast search, rename the columns.

blast <- mutate(blast, start_to_end=(ifelse(qstart<qend, paste(qstart, "-", qend,sep=''), paste(qend, "-",qstart, sep='' ))))
#add a column "start-to-end" we'll need it for emboss substringing later
blast <- blast %>% mutate(strand=ifelse(sign(qframe)==1, "+", "-"))
#indicate which strand the hit is found on.
blast <- select(blast, HE, evalue, bitscore, start_to_end, strand)

args <- commandArgs(TRUE)
e_or_bitscore <- args[1]
cutoff <- as.numeric(args[2])
filename <- args[3]
#take 3 command line args: whether to use e val or bitscore, the cutoff, and the filename prefix for our graph/table outputs. 

if (e_or_bitscore=="e"){
    blast <- blast %>% arrange(evalue) %>% mutate(cutoffmet = ifelse(evalue<cutoff, "Significant", "Not Significant"))
#arrange by evalue. We'll use cutoffmet for the graphs in a few steps. 
    blast <- tibble::rowid_to_column(blast, "ID")
#add an ID column.
    blastfiltered <- blast %>% filter(evalue < cutoff) 
#take only those that met cutoff
    p<- ggplot(blast, aes(x=ID, y=evalue))+ geom_point()+
        geom_point(data=blastfiltered, aes(x=ID, y=evalue), shape=3)
   ggsave(paste(filename, "plot.png", sep=''), plot=p)
#makes a plot of ID vs evalue, where those points that meet the significance cutoff are a different shape
   fullblastplot <-plot_ly(blast, x= ~ID, y= ~evalue, 
        type= "scatter", text=~paste("position in genome: ", start_to_end, "strand: ", strand, "HE match: ", HE, sep="<br>"), color = ~cutoffmet)
   fullblastplot <- fullblastplot %>% layout(hovermode="closest")
#interactive graph of all hits. colored by whether cut off is met. on hover, shows genome position, strand, and HE match accession 
    filteredplot <-plot_ly(blastfiltered, x= ~ID, y= ~evalue, 
        type= "scatter", text=~paste("position in genome: ", start_to_end, "strand: ", strand, "HE match: ", HE, sep="<br>"), color = ~cutoffmet) 
#same plot but with only the significant hits (useful when dealing with a very large query, in which diplaying every hit can make performance slow
} else {
#if we're dealing with bitscore:
    blast <- blast %>% arrange(desc(bitscore)) %>% mutate(cutoffmet = ifelse(bitscore>cutoff, TRUE, FALSE))
    blast <- tibble::rowid_to_column(blast, "ID")
#add an ID column.
    blastfiltered <- blast %>% filter(bitscore > cutoff) 

    p<- ggplot(blast, aes(x=ID, y=bitscore))+ geom_point()+
        geom_point(data=blastfiltered, aes(x=ID, y=bitscore), shape=3)
   ggsave(paste(filename, "plot.png", sep=''), plot=p)
#makes a plot of ID vs bitscore, where those points that meet the significance cutoff are a different color
   fullblastplot <-plot_ly(blast, x= ~ID, y= ~bitscore, 
        type= "scatter", text=~paste("position in genome: ", start_to_end, "strand: ", strand, "HE match: ", HE, sep="<br>"), color = ~cutoffmet)
   fullblastplot <- fullblastplot %>% layout(hovermode="closest")
#make same interactive plots as the evalue section. this is admittedly not very dry code. 
    filteredplot <-plot_ly(blastfiltered, x= ~ID, y= ~bitscore, 
        type= "scatter", text=~paste("position in genome: ", start_to_end, "strand: ", strand, "HE match: ", HE, sep="<br>"), color = ~cutoffmet) 
}
#save all the plots, using whatever file name prefix was supplied by the user
htmlwidgets::saveWidget(fullblastplot, paste(filename, "full_blast_interactiveplot.html", sep=''), selfcontained=FALSE)
htmlwidgets::saveWidget(filteredplot, paste(filename, "filtered_interactiveplot.html", sep=''), selfcontained=FALSE)
write.table(blastfiltered, file=paste(filename, "_filtered", sep=''), sep="\t")
blastfiltered$start_to_end %>% write.table(file="start_to_end.txt", col.names= FALSE, quote=FALSE)
write.table(blast, file=paste(filename, "_full", sep=''), sep="\t")
