#install.packages('ggplot2')
#install.packages("tidyverse")

library(ggplot2)
library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
TRA_path <- args[1]
TRB_path <- args[2]
outdir <- args[3]
sample_name <- args[4]

TRA <- data.table::fread(TRA_path)
TRB <- data.table::fread(TRB_path)

TRA_data <- data.frame(vGene=sort(unique(TRA$vGene)))
umi_count <- c()
for (gene in sort(unique(TRA$vGene))) {
  umi_count <- c(umi_count, sum(TRA[TRA$vGene == gene,]$totalUMICount))
}
TRA_data$value <- umi_count

TRB_data <- data.frame(vGene=sort(unique(TRB$vGene)))
umi_count <- c()
for (gene in sort(unique(TRB$vGene))) {
  umi_count <- c(umi_count, sum(TRB[TRB$vGene == gene,]$totalUMICount))
}
TRB_data$value <- umi_count


p_a <- ggplot(TRA_data, aes(x=vGene, y=value)) +
    ggtitle("Unique Clonotypes for each TRAV Genes") +
    geom_bar(position='dodge',stat='identity', fill='steelblue') + 
    ylab("Number of Unique Clonotypes") + 
    xlab("Productive V Genes") + 
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

TRA_sample <- paste("/",sample_name,"_TRAV.png", sep="")
TRA_output <- paste(outdir, TRA_sample, sep="")
ggsave(TRA_output,plot=p_a, width = 30, height = 20, units = "cm", bg='white')

p_b <- ggplot(TRB_data, aes(x=vGene, y=value)) +
    ggtitle("Unique Clonotypes for each TRBV Genes") +
    geom_bar(position='dodge',stat='identity', fill='steelblue') + 
    ylab("Number of Unique Clonotypes") + 
    xlab("Productive V Genes") + 
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

TRB_sample <- paste("/", sample_name,"_TRBV.png",sep="")
TRB_output <- paste(outdir, TRB_sample,sep="")
ggsave(TRB_output,plot=p_b, width = 30, height = 20, units = "cm", bg='white')

