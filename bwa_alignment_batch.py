#This python script generates shell script containing PBS directives and submit jobs to the PBS queue.
# One PBS script is generated for each pair of fastq file. The PBS directives can be contolled within the python script.

import os, glob
import sys,re,fileinput

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 3:	
	print "Usage: Input_directory Job_Script_directory Output_directory" 
	sys.exit()
  
dpath = Argument[0]
Listoffile = []

def dir(patharray):
    Listdir = []
    for infile in patharray:
        Listdir.append(os.path.join(dpath,infile))
    return Listdir    

Listoffile = dir(os.listdir(dpath))
#print Listoffile

Fastq = {}

for Filepath in Listoffile:
	for (path, dirs, files) in os.walk(Filepath):
		for file in files:
			if file.endswith("_1.fastq.gz") and not os.path.getsize(path+"/"+file) == 0:
				if path+"/"+file not in Fastq:
					Fastq[path+"/"+file] = (path+"/"+file).replace("_1.fastq.gz","_2.fastq.gz")

print Fastq
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

if not os.path.exists(str(Argument[2])):
	os.makedirs(str(Argument[2]))

for file in Fastq:

	dirname = ""
	fastq_name1 = ""
	fastq_name2 = ""

	info1 = []
	info1 = file.split("/")

	info2 = []
	info2 = Fastq[file].split("/")
	
	dirname = info1[-1].replace("_1.fastq.gz","")
	print dirname

	aln_name1 = info1[-1].replace(".fastq.gz",".sai")
	aln_name2 = info2[-1].replace(".fastq.gz",".sai")

	if not os.path.exists(str(Argument[2])+"/"+str(dirname)):
                os.makedirs(str(Argument[2])+"/"+str(dirname))
	
	#print aln_name1
	#print aln_name2

	jobfile1 = ""
	jobfile2 = ""

	jobname1 = ""
	jobname1 = str(Argument[1])+"/"+re.sub(r'\s','',str((info1[-1]).replace(".fastq.gz",""))+".sh")
	jobfile1 = open(str(jobname1),"w")
	
	jobfile1.write("#!/bin/bash\n#PBS -l walltime=120:00:00\n#PBS -l nodes=1:ppn=8\n#PBS -N BWA_Alignment_"+str(aln_name1)+"\n\nSTART=$(date +%s)\n\n/home/apandey/bio/bwa-0.6.2/bwa aln -t 8 -q 15 -n 6 -k 2 -l 25 /home/apandey/Reference_Fasta/mm10/bwa_index/mm10_ucsc.fa "+str(file)+"  >  "+str(Argument[2])+"/"+str(dirname)+"/"+str(aln_name1)+"\nEND=$(date +%s)\nDIFF=$(( $END - $START ))\n\necho \"It took $DIFF seconds\"\n")	
	jobfile1.close()


	jobname2 = ""
        jobname2 = str(Argument[1])+"/"+re.sub(r'\s','',str((info2[-1]).replace(".fastq.gz",""))+".sh")
        jobfile2 = open(str(jobname2),"w")

        jobfile2.write("#!/bin/bash\n#PBS -l walltime=120:00:00\n#PBS -l nodes=1:ppn=8\n#PBS -N BWA_Alignment_"+str(aln_name2)+"\n\nSTART=$(date +%s)\n\n/home/apandey/bio/bwa-0.6.2/bwa aln -t 8 -q 15 -n 6 -k 2 -l 25 /home/apandey/Reference_Fasta/mm10/bwa_index/mm10_ucsc.fa "+str(Fastq[file])+"  >  "+str(Argument[2])+"/"+str(dirname)+"/"+str(aln_name2)+"\nEND=$(date +%s)\nDIFF=$(( $END - $START ))\necho \"It took $DIFF seconds\"\n")
	jobfile2.close()

	print "qsub "+str(jobname1)
	print "qsub "+str(jobname2)

	os.system("qsub "+str(jobname1))
	os.system("qsub "+str(jobname2))


