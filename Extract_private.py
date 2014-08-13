## This program extracts the private variants for a given strain from the Sanger 18 strains vcf file (MGP)

import re,sys,fileinput

Argument = []
Argument = sys.argv[1:] 

Filepath = Argument[0]
Strain_column = int(Argument[1])
Outpath = Argument[2]


newfile = open(str(Outpath),"w")

for line in fileinput.input([Filepath]):
	if line.startswith("#"):
		newfile.write(str(line))
		continue
		
        rowlist = []
        rowlist = line.split("\t")

	genotype = []	
	genotype = rowlist[Strain_column].split(":")

	Variant = "No"

    	if genotype[-1] == "1":
		if genotype[0] == "1/1": 
			Variant = "Yes"	

	
	rowlist[Strain_column] = "NA"
	
	Other_strains = []

	for geno in rowlist[9:]:
		if geno == "NA":
			continue

		genotype = []
		genotype = geno.split(":")[0]
		if genotype == "0/0":
 			Other_strains.append(genotype)


	if len(Other_strains) == 17 and Variant == "Yes":
		newline = ""
                newline = line
                newfile.write(str(newline))

newfile.close()
        
    

    

    
