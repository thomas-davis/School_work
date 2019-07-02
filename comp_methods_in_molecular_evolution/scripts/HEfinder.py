import argparse
import os 
#argparse handles command line arguments. os lets us call the terminal from out program
parser =argparse.ArgumentParser()
parser.add_argument("genome", help="Genome to search for homing endonucleasess") 
parser.add_argument("-use_bitscore", help="use evalue or bitscore for filtering (default evalue)", action="store_true", default=False)
parser.add_argument("-o", help="make multiple sequence file out of significant sections of query", action="store_true", default=True) 
parser.add_argument("-c", help="evalue or biscore cutoff to be used", type=int, default=None)
parser.add_argument("-name", help="prefix name of output files", default="blast")
args=parser.parse_args()
if args.use_bitscore and args.c is None:
 args.c=50
elif args.c is None: 
 args.c=1
#if we're using bitscore and no cutoff is specified, use 50. If we're using E-value, default is 1
if args.use_bitscore: 
 e_or_bit="b" 
else: 
 e_or_bit="e"
print(args)
os.system("./hefinder.sh {} {} {} {}".format(args.genome, e_or_bit, args.c, args.name))
#call hefinder that runs blast, and parses blast output to make graphs.
if args.o: 
#if the user wants the significant sections of genome
 start_and_end_points=[]
 with open("start_to_end.txt", "r") as f: 
#start_and_end is created by the blast parse program. It contains the start and end points of the significant sequences of the genome
  for line in f: 
   start_and_end=line.split()[1]
   start_and_end_points.append(start_and_end)
#read in the start and end points
 start_and_end_points=list(set(start_and_end_points))
 start_and_end_points=(' '.join(start_and_end_points)) 
 os.system("extractseq {} {} -reg '{}' -separate ".format(args.genome, args.name+"_significant_hit_sequences.seq", start_and_end_points ))
#here we use emboss extractseq to substring out the significant sections of genome (it automatically deals with header lines, and does everything very quickly)
#we write out the resut to name_significant_hit_sequences.seq
 os.system("rm start_to_end.txt")
#clean up, getting rid of the start_and_end file we used to substringing.
