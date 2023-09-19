import string,sys,os
  
def step1_peaks():
    #VEH_OSI
    os.system('bedtools intersect -a VEH_S1_peaks.narrowPeak -b OSI_S7_peaks.narrowPeak -v > VEH_OSI.specific.out')
    os.system('bedtools intersect -a OSI_S7_peaks.narrowPeak -b VEH_S1_peaks.narrowPeak -v > OSI_VEH.specific.out')
    os.system('bedtools intersect -a VEH_S1_peaks.narrowPeak -b OSI_S7_peaks.narrowPeak -wa > VEH_OSI.overlap.out')

def step2_summits():
    os.system('bedtools intersect -a VEH_S1_summits.bed -b OSI.specific.out -wa > VEH_OSI.specific2.out')
    os.system('bedtools intersect -a VEH_S1_summits.bed -b OSI.overlap.out -wa > VEH_OSI.overlap2.out')
    os.system('bedtools intersect -a OSI_S7_summits.bed -b VEH.specific.out -wa > OSI_VEH.specific2.out')

def step3_input():
  #ONT_specific
  chr1    10061   10062   975-ONT_S2_peak_1       7.68425
  #Overlap
  chr1    11323   11324   975-VEH_S1_peak_2       7.06657
  #VEH_specific
  chr1    10578   10579   975-VEH_S1_peak_1       6.1468
    os.system('cat OSI_VEH.specific2.out VEH_OSI.overlap2.out VEH_OSI.specific2.out > VEH_OSI.sum.bed')


def step4_Heatmap():
    #Deeptools
    os.system('computeMatrix reference-point --referencePoint center -S VEH_S1_dedup.bw OSI_S7_dedup.bw -R VEH_OSI.sum.bed -b 2000 -a 2000 --skipZeros --numberOfProcessors 96 -o VEH_OSI_peaks.subtractCPM.gz --outFileSortedRegions VEH_OSI_peaks.subtractCPM.bed')
    os.system('plotHeatmap --colorList white,darkred  --plotFileFormat pdf   --samplesLabel VEH ONT  --plotTitle "" -m VEH_OSI_peaks.subtractCPM.gz -out VEH_OSI_peaks.subtractCPM.heatmap.pdf --xAxisLabel "" ')

def main():
    #step1_peaks()
    #step2_summits()
    #step3_input()
    step4_Heatmap()

if __name__ == "__main__":
    main()
