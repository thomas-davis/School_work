#this program takes the output of the last round of a psiblast as input, and reads through the accession numbers, using biopython to find the corresponding amino acid fasta sequence for each accession. It writes these sequences out to a file
import subprocess
from Bio import Entrez, SeqIO, Seq
filename=str(input("enter a name for the final multiple fasta file: "))
file_to_parse=input("name of input file: ")
#get the file to be parsed and output file name from the user. 
accession_list=subprocess.check_output(["grep", "-o", "|.*|", file_to_parse])
#In psiblast output, accesion IDs are always surrounded by | |. here we grep out everything surrounded by ||. there are possibly better ways to do this with python regex, I did this for simplicity. 
accession_list=accession_list.replace("\n","")
accessions=set(tester.split("|"))  
#we split it on | to obtain a list of IDS. we bounce those IDs through a set, which keeps only unique IDS. 
Entrez.email = "thomas.davis@uconn.edu" 
fastalist=[]
for idstr in accesions:
#iterate through the list of IDs
 if idstr:
  idstr.replace("|","")
  try:
#attempt to look up the ID in the entrez protein database.
   handle = Entrez.efetch(db="protein", id=idstr, rettype="gb", retmode="text")
   record = SeqIO.read(handle, "genbank")
   fasta=[">", "|", idstr,"|", (record.description+"\n"), (str(record.seq)+"\n")]
#add a header with the accession number, description, and the sequence. 
   fastalist.append(''.join(fasta))
   handle.close()
  except: 
   print("following ID line could not be parsed" {}.format(idstr)) 
#if we can't read an ID, we print the line that could not be parsed 
fh=open(filename, "w")
for fasta in fastalist: 
 fh.write(fasta)
#write out fasta out to a file
fh.close()
