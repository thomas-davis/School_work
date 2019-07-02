import sys
##program description:
#initialize a node for each weight. For each node compare to the nodes after it.
#check to see if the difference between current and next is an amino acid
#if it is, check if the peptide that would be formed by the AAs addition to the peptide in the current node
#is longer than the peptide already stored at the next node
#if this peptide would be longer, set next peptide to it.
#at the end, return the longest peptide in the DAG

#here's the problem http://rosalind.info/problems/sgra/?class=527

class Node:
    def __init__(self, weight):
        '''class representing the nodes of our DAG'''
        self.weight=weight
        self.peptide=''
    def __len__(self):
        return len(self.peptide)
    def __repr__(self):
        return str(self.weight)+" "+self.peptide
    def __sub__(self, other):
        '''round mass difference to 2 decimal places'''
        return round(self.weight-other.weight, 2)

def generate_dict():
    '''make dict mapping mass to AA'''
    AA_masses="""A   71.03711
C   103.00919
D   115.02694
E   129.04259
F   147.06841
G   57.02146
H   137.05891
I   113.08406
K   128.09496
L   113.08406
M   131.04049
N   114.04293
P   97.05276
Q   128.05858
R   156.10111
S   87.03203
T   101.04768
V   99.06841
W   186.07931
Y   163.06333"""
    AA_masses=AA_masses.split()
    masses=AA_masses[1::2]
    masses=[round(float(a),2) for a in masses]
    AA_masses=dict(zip(masses,(AA_masses[0::2])))
    return AA_masses

if __name__=="__main__":
    AA_dict=generate_dict()
    filename=sys.argv[1]
    fh=open(filename, "r")
    L=fh.read()
    fh.close()
    L=L.strip().split()
    L=list(map(float, L))
    #get file of masses, and covert it into a list of masses
    graph=[Node(weight) for weight in L]
    for i in range(len(L)):
        for j in range(i, len(L)):
            current, next = graph[i], graph[j]
            mass_difference=next-current
            if mass_difference in AA_dict:
                if len(current)+1 >len(next):
                    #if there is a longer path to the next node, update it.
                    AA=AA_dict[mass_difference]
                    next.peptide=current.peptide+AA
    longest_node=(max(graph, key=lambda x: len(x)))
    print(longest_node.peptide)
