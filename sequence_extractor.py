## This program takes reference fasta file and input file (bed format) and extracts corresponding genomic sequences. It takes care of the strand specificity and outputs reverse complement when strand is negative.
## samtools faidx can now do this job much fastly. This script was written few years back when there were a very few options to extract sequences. 


import os, sys, fileinput

Argument = []
Argument = sys.argv[1:]

if (len(Argument)) < 1:
        print "Usage:Inputfile Fastafile Outputfile"
        sys.exit()

Fasta = {}

def reversecomplement(sequence):
    """Return the reverse complement of the dna string.""" 

    complement = {"A":"T", "T":"A", "C":"G", "G":"C", "N":"N"}
    
    reverse_complement_sequence = ""

    sequence_list = list(sequence)
    sequence_list.reverse()

    for letter in sequence_list:
        reverse_complement_sequence += complement[letter.upper()]
    
    return reverse_complement_sequence
    

output = open(Argument[2],"w")

linestring = open(Argument[1], 'r').read()

fasta = []
fasta = linestring.split("\n>")

for i in fasta:
	if i.split("\n")[0].strip(">") not in Fasta:
		Fasta[(i.split("\n")[0].strip(">")).lstrip("chr")] = "".join(i.split("\n")[1:])

for line in fileinput.input([Argument[0]]):
        if line.startswith("#"):
                continue

        array = []
        line = line.rstrip("\n")
	array = line.split("\t")

	chrome = ""
	strand = ""
	start = 0
	end = 0

	chrome = array[1].lstrip("chr")
	strand = array[2]
	start = array[3]
	end = array[4]
	
	if strand != "+" and strand != "-":
		output.write(str(line)+"\n")
		continue

	if strand == "+":
		output.write(str(line)+"\t"+str(Fasta[str(chrome)][int(start):int(end)])+"\n")
	else:
		output.write(str(line)+"\t"+str(reversecomplement(Fasta[str(chrome)][int(start):int(end)]))+"\n")

output.close()
