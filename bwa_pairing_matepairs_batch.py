import os, glob
import sys,re,fileinput

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 3:	
	print "Usage: Input_directory_sai  Job_Script_directory Output_directory Input_directory_fastq" 
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

Sai = {}

for Filepath in Listoffile:
	for (path, dirs, files) in os.walk(Filepath):
		for file in files:
			if file.endswith("_1.sai") and not os.path.getsize(path+"/"+file) == 0:
				if path+"/"+file not in Sai:
					Sai[path+"/"+file] = (path+"/"+file).replace("_1.sai","_2.sai")

print Sai
									
if not os.path.exists(str(Argument[2])):
	os.makedirs(str(Argument[2]))


if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

for file in Sai:
	
	dirname = ""
	samfile = ""

	info = []
	info = file.split("/")

	pinfo = []
	pinfo = Sai[file].split("/")

	dirname = info[-2]
	print dirname
	samfile = info[-2]+".sam"

	if not os.path.exists(str(Argument[2])+"/"+str(dirname)):
                os.makedirs(str(Argument[2])+"/"+str(dirname))
	
	jobfile = ""
	jobname = str(Argument[1])+"/"+re.sub(r'\s','',str(dirname)+"_sam.sh")
	jobfile = open(str(jobname),"w")


	fastq1 = ""
	fastq2 = ""
	
	fastq1 = Argument[3]+"/"+str(dirname)+"/"+(info[-1]).replace(".sai",".fastq.gz")
	fastq2 = Argument[3]+"/"+str(dirname)+"/"+(pinfo[-1]).replace(".sai",".fastq.gz")

	#print fastq1

	jobfile.write("#!/bin/bash\n#PBS -l walltime=120:00:00\n#PBS -l nodes=1:ppn=6\n#PBS -N BWA_mate_pairing_"+str(dirname)+"\n\nSTART=$(date +%s)\n\n/home/apandey/bio/bwa-0.6.2/bwa sampe  /home/apandey/Reference_Fasta/mm10/bwa_index/mm10_ucsc.fa -r \'@RG\\tID:"+str(dirname)+"\\tSM:DBA2_J\' "+str(file)+"    "+str(Sai[file])+"  "+str(fastq1)+" "+str(fastq2)+"   > "+str(Argument[2])+"/"+str(dirname)+"/"+str(samfile)+"\n\nEND=$(date +%s)\nDIFF=$(($END - $START))\necho \"It took $DIFF seconds\n")
	jobfile.close()

	print "qsub "+str(jobname)
	os.system("qsub "+str(jobname))



