STEP1_ChIPseeker <- function(){
        #BiocManager::install('ChIPseeker')
        library(ChIPseeker)
        library(org.Hs.eg.db)
        library(TxDb.Hsapiens.UCSC.hg38.knownGene)
        txdb = TxDb.Hsapiens.UCSC.hg38.knownGene

        bed = read.table("sum.bed", header=T)
        peaks.gr = makeGRangesFromDataFrame(bed, keep.extra.columns=TRUE)
        peakAnno  = annotatePeak(peaks.gr,tssRegion=c(-3000,3000), TxDb=txdb, annoDb="org.Hs.eg.db")
        plotAnnoPie(peakAnno,cex =1.1) #legend size
        peak.anno = as.data.frame(peakAnno)
        write.table(peak.anno, file='sum.anno.txt',row.names=FALSE,quote=FALSE,sep='\t')
}
