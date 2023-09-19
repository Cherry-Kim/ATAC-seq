import string,sys,os,glob

def STEP0_Preprocessing(sample):
    os.system('fastqc -t 48 --nogroup '+sample+'_R1_001.fastq.gz')
    os.system('trim_galore  -j 96 --fastqc --gzip -o trim_galore/ '+sample+'_R1_001.fastq.gz')

def STEP1_MAPPING(sample,REF,SP):
    os.system('bowtie2 -p 48 -x '+REF+SP+' -1 trim_galore/'+sample+'_R1_val_1.fq.gz -2 trim_galore/'+sample+'_R2_val_2.fq.gz -S '+sample+'.sam 2>'+sample+'.bowtie2Log')
    #os.system('bowtie2 -p 96 -x '+REF+SP+' -U trim_galore/'+sample+'_R1_001_trimmed.fq.gz -S '+sample+'.sam 2>'+sample+'.bowtie2Log')
    os.system('samtools view -bS '+sample+'.sam > '+sample+'.bam')
    os.system('samtools sort --threads 96 '+sample+'.bam > '+sample+'.sorted.bam')
    os.system('samtools index '+sample+'.sorted.bam')
    os.system('samtools flagstat '+sample+'.sorted.bam > '+sample+'.flagstat')

def STEP2_FILTER(sample,REF,SP):
    ##os.system('bamtools filter -in '+sample+'.sorted.bam -out '+sample+'.filterd.bam -mapQuality ">=30" -isProperPair true')
    os.system('samtools view '+sample+'.sorted.bam | egrep -v chrM | samtools view -bT '+REF+SP+'.fa -o '+sample+'.-chrM.bam')

    if not os.path.isdir('TEMP_PICARD'):
        os.mkdir('TEMP_PICARD')
    os.system('java -Xmx8g -jar /BIO1/picard.jar MarkDuplicates TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT I='+sample+'.-chrM.bam O='+sample+'.dedup.sam M='+sample+'.duplicate_metrics REMOVE_DUPLICATES=true AS=true')
    os.system('java -Xmx8g -jar /BIO1/picard.jar SortSam TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I='+sample+'.dedup.sam O='+sample+'_dedup.bam CREATE_INDEX=true')

    os.system('bamCoverage -b '+sample+'_dedup.bam -o '+sample+'_dedup.bw')

def STEP3_PEAK_CALL(sample):
    os.system('bedtools bamtobed -i '+sample+'_dedup.bam  > '+sample+'.bed')
    os.system('macs2 callpeak -t '+sample+'.bed -n '+sample+' -g hs -B -q 0.05 --outdir macs2_'+sample+' --nomodel --shift -100 --extsize 200')

    os.system('bedtools intersect -v -a macs2_'+sample+'/'+sample+'_peaks.narrowPeak -b GRCh38_unified_blacklist.bed > '+sample+'_peaks.narrowPeak.filt')

def STEP4_PEAK_ANNOTATION(sample,REF,GTF):
    os.system('awk -F "\t" \'{print $4 "\t" $1 "\t" $2 "\t" $3 "\t" "+"}\' '+sample+'_peaks.narrowPeak.filt > '+sample+'.input.bed')
    os.system('perl /BIO1/homer/bin/annotatePeaks.pl '+sample+'.input.bed '+REF+' -gtf '+GTF+' > '+sample+'_annotations.txt')

def STEP5_DASTK():
    file_list = os.listdir('./')
    peak_list = sorted([file for file in file_list if file.endswith('_peaks.narrowPeak.filt')])
    #for i in peak_list:
    #    print(i)
        #if not os.path.isdir('DASTK_'+i):
        #    os.mkdir('DASTK_'+i)
        #os.system('python3 /BIO1/DAStk/DAStk/process_atac.py -t 96 -e '+i+' -m /BIO1/REF/hg38/grch38_motifs/ -g hg38 -o DASTK_'+i)

    os.system('python3 /BIO1/DAStk/DAStk/differential_md_score.py -1 DASTK_S4_peaks.narrowPeak.filt/S4_peaks.narrowPeak_md_scores.txt -2 DASTK_S2_peaks.narrowPeak.filt/S2_peaks.narrowPeak_md_scores.txt  -p 0.05 -m "Group1" -n "Group2" -b -o DASTK_differential_md_score') #-1:control -2:case
   
    #fpout = open('header.out','w')
    #a = ['#Motif name','p-value','#total motif hits','#nearby peaks in condition 1','#nearby peaks in condition 2']
    #fpout.write('\t'.join(a)+'\t'+'MD-score in 827-ONT'+'\t'+'MD-score in 975-ONT'+'\t'+'differential MD-score'+'\n')
    os.system('cat header.out DASTK_differential_md_score/8S4_peaks.narrowPeak_vs_S2_peaks.narrowPeak_differential_md_scores.txt > S4_peaks.narrowPeak_vs_S2_peaks.narrowPeak_differential_md_scores.head.txt')
      

def STEP6_DIFFBIND():
    r.source("2.DiffBind.R")

def main():
    REF,SP,GTF,co,path = '/BIO1/REF/hg38/','hg38','/BIO1/REF/hg38/hg38.refGene.gtf',0,'./'
    file_list = os.listdir(path)
    fq_list = sorted([file for file in file_list if file.endswith('_R1_001.fastq.gz')])
    for i in fq_list:
        co += 1
        sample = i.split('_R1_001.fastq.gz')[0]
        print(co,sample)
        STEP0_Preprocessing(sample)
        STEP1_MAPPING(sample,REF,SP)
        STEP2_FILTER(sample,REF,SP)
        STEP3_PEAK_CALL(sample)
        #STEP4_PEAK_ANNOTATION(sample,REF,GTF)
    STEP5_DASTK()
    #STEP6_DIFFBIND()
main()
