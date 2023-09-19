import string,sys,os
  
def step1_peaks():
    #VEH_OSI
    os.system('bedtools intersect -a 975-VEH_S1_peaks.narrowPeak -b 975-OSI_S7_peaks.narrowPeak -v > VEH_OSI.specific.out')
    os.system('bedtools intersect -a 975-OSI_S7_peaks.narrowPeak -b 975-VEH_S1_peaks.narrowPeak -v > OSI_VEH.specific.out')
    os.system('bedtools intersect -a 975-VEH_S1_peaks.narrowPeak -b 975-OSI_S7_peaks.narrowPeak -wa > VEH_OSI.overlap.out')

def step2_summits():
    os.system('bedtools intersect -a 975-VEH_S1_summits.bed -b VEH_OSI.specific.out -wa > VEH_OSI.specific2.out')
    #chr1    10150   10151   827-VEH_S1_peak_1       41.3352
    #chr1    181391  181632  827-VEH_S1_peak_14      70      .       3.36226 8.99646 7.02083 83
    #chr1    181474  181475  827-VEH_S1_peak_14      7.02083
    os.system('bedtools intersect -a 975-VEH_S1_summits.bed -b VEH_OSI.overlap.out -wa > VEH_OSI.overlap2.out')
    os.system('bedtools intersect -a 975-OSI_S7_summits.bed -b OSI_VEH.specific.out -wa > OSI_VEH.specific2.out')

def step3_input():
  #ONT_specific
  chr1    10061   10062   975-ONT_S2_peak_1       7.68425
  #Overlap
  chr1    11323   11324   975-VEH_S1_peak_2       7.06657
  #VEH_specific
  chr1    10578   10579   975-VEH_S1_peak_1       6.1468
    os.system('cat OSI_VEH.specific2.out VEH_OSI.overlap2.out VEH_OSI.specific2.out > VEH_OSI.sum.bed')
    os.system('cat ONT_VEH.specific2.out VEH_ONT.overlap2.out VEH_ONT.specific2.out > VEH_ONT.sum.bed')
    os.system('cat TRC_VEH.specific2.out VEH_TRC.overlap2.out VEH_TRC.specific2.out > VEH_TRC.sum.bed')

