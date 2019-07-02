#!/bin/bash
genome=$1
e_or_bit=$2
cutoff=$3
name=$4
module load blast/2.3.0
module load R/3.3.1

blastx -query $genome -db Combined_homing_endonuclease_database.faa -culling_limit 1 -out blast.txt -outfmt " 6 sacc evalue bitscore qstart qend qframe" -evalue 10.1
Rscript blastparse.R $e_or_bit $cutoff $name
 





