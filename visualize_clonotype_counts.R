library(ggplot2)
library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
TRA_path <- args[1]
TRB_path <- args[2]
outdir <- args[3]
sample_name <- args[4]

TRA <- data.table::fread(TRA_path)
TRB <- data.table::fread(TRB_path)

Total_TRA <- paste("Total Number of Unique Clonotypes:",TRA$Unique_Clonotypes[1])
Total_TRB <- paste("Total Number of Unique Clonotypes:",TRB$Unique_Clonotypes[1])

TRA_data <- data.frame(table(TRA$vGene))
TRB_data <- data.frame(table(TRB$vGene))


p_a <- ggplot(TRA_data, aes(x=Var1, y=Freq)) +
    labs(title = "Unique Clonotypes for each TRAV Genes", subtitle = Total_TRA) + 
    #ggtitle(paste("Unique Clonotypes for each TRAV Genes /", Total_TRA)) +
    geom_bar(position='dodge',stat='identity', fill='steelblue') + 
    ylab("Number of Unique Clonotypes") + 
    xlab("Productive V Genes") + 
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, face="bold"))

TRA_sample <- paste("/",sample_name,"_TRAV.png", sep="")
TRA_output <- paste(outdir, TRA_sample, sep="")
ggsave(TRA_output,plot=p_a, width = 30, height = 20, units = "cm", bg='white')

p_b <- ggplot(TRB_data, aes(x=Var1, y=Freq)) +
    labs(title = "Unique Clonotypes for each TRBV Genes", subtitle = Total_TRB) + 
    #ggtitle(paste("Unique Clonotypes for each TRBV Genes / ",Total_TRB)) +
    geom_bar(position='dodge',stat='identity', fill='steelblue') + 
    ylab("Number of Unique Clonotypes") + 
    xlab("Productive V Genes") + 
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, face="bold"))

TRB_sample <- paste("/", sample_name,"_TRBV.png",sep="")
TRB_output <- paste(outdir, TRB_sample,sep="")
ggsave(TRB_output,plot=p_b, width = 30, height = 20, units = "cm", bg='white')

