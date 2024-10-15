library( "DESeq2" )
library(ggplot2)

AvsC=FALSE
if (AvsC){
    PATH_COUNT='genecount_matrix-2.csv'
    PATH_META='metadata-2.csv'
    PATH_OUTPUT="A-vs-C.csv"
    PATH_IMAGE="Volcano_AC.pdf"
} else{
    PATH_COUNT='genecount_matrix-1.csv'
    PATH_META='metadata-1.csv'
    PATH_OUTPUT="A-vs-B.csv"
    PATH_IMAGE="Volcano_AB.pdf"
}



setwd("/Users/deng/Research/Fredrick007/gene_counts_feature")
countData <- read.csv(PATH_COUNT, header = TRUE, sep = ",")
head(countData)



metaData <- read.csv(PATH_META, header = TRUE, sep = ",")
metaData

dds <- DESeqDataSetFromMatrix(countData=countData, 
                              colData=metaData, 
                              design=~dex, tidy = TRUE)
dds <- DESeq(dds)

res <- results(dds)
head(results(dds, tidy=TRUE))

write.csv(as.data.frame(res), 
          file=PATH_OUTPUT)

summary(res)

# Volcano plot
#reset par
par(mfrow=c(1,1))
# Make a basic volcano plot
with(res, plot(log2FoldChange, -log10(pvalue), pch=20, main="Volcano plot", xlim=c(-3,3)))

# Add colored points: blue if padj<0.01, red if log2FC>1 and padj<0.05)
with(subset(res, padj<.01 ), points(log2FoldChange, -log10(pvalue), pch=20, col="blue"))
with(subset(res, padj<.01 & abs(log2FoldChange)>2), points(log2FoldChange, -log10(pvalue), pch=20, col="red"))


