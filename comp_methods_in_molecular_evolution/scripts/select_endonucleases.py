file= str(input("please enter the name of the file to be parsed: "))
fh=open(file+"endonucleases", "w")
with open(file, "r") as f: 
 for fasta in f:
  if "homing endonuclease" in fasta:
#check to see if its annotated as a homing endonuclease
   fh.write(fasta)
#if it is write it to a fil
fh.close()
 
