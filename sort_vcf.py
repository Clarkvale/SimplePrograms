## This program takes moouse vcf file and sorts them based on chromosomal location 
## can be easily modified for any other species

import os, sys

Argument = []
Argument = sys.argv[1:]

if (len(Argument)) < 1:
        print "Usage:Input_Fasta Outputfile"
        sys.exit()

Fasta = {}

output = open(Argument[1],"w")

input = open(Argument[0])

Extra_chromosomes = ['chr1_GL456210_random',
'chr1_GL456211_random',
'chr1_GL456212_random',
'chr1_GL456213_random',
'chr1_GL456221_random',
'chr4_GL456216_random',
'chr4_GL456350_random',
'chr4_JH584292_random',
'chr4_JH584293_random',
'chr4_JH584294_random',
'chr4_JH584295_random',
'chr5_GL456354_random',
'chr5_JH584296_random',
'chr5_JH584297_random',
'chr5_JH584298_random',
'chr5_JH584299_random',
'chr7_GL456219_random',
'chrX_GL456233_random',
'chrY_JH584300_random',
'chrY_JH584301_random',
'chrY_JH584302_random',
'chrY_JH584303_random',
'chrUn_GL456239',
'chrUn_GL456359',
'chrUn_GL456360',
'chrUn_GL456366',
'chrUn_GL456367',
'chrUn_GL456368',
'chrUn_GL456370',
'chrUn_GL456372',
'chrUn_GL456378',
'chrUn_GL456379',
'chrUn_GL456381',
'chrUn_GL456382',
'chrUn_GL456383',
'chrUn_GL456385',
'chrUn_GL456387',
'chrUn_GL456389',
'chrUn_GL456390',
'chrUn_GL456392',
'chrUn_GL456393',
'chrUn_GL456394',
'chrUn_GL456396',
'chrUn_JH584304']

def numeric_compare(x, y):
	x1 = int(x)
	y1 = int(y)
	return x1 - y1

Chromosome = ["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chrX"]

VCF = {}

for line in input:
        if line.startswith("#"):
                output.write(str(line))
                continue

        v = []
        v = line.strip("\n").split("\t")

	if v[0] not in VCF:
		VCF[v[0]] = {}
		VCF[v[0]][v[1]] = line
	else:
		VCF[v[0]][v[1]] = line

All_chr = []
All_chr = Chromosome + Extra_chromosomes

for chr in All_chr:
	for pos in sorted(VCF[chr].keys(),cmp=numeric_compare):
		output.write(str(VCF[chr][pos]))
		output.flush()	
output.close()
