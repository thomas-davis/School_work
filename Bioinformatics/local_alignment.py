#For a weighted alphabet A and a collection L of positive real numbers, the spectrum graph of L is a digraph constructed in the following way. First, create a node for every real number in L. Then, connect a pair of nodes with a directed edge (u,v) if v>u and v−u is equal to the weight of a single symbol in A. We may then label the edge with this symbol.

#In this problem, we say that a weighted string s=s1s2⋯sn matches L if there is some increasing sequence of positive real numbers (w1,w2,…,wn+1) in L such that w(s1)=w2−w1, w(s2)=w3−w2, ..., and w(sn)=wn+1−wn.

#Given: A list L (of length at most 100) containing positive real numbers.

#Return: The longest protein string that matches the spectrum graph of L (if multiple solutions exist, you may output any one of them). Consult the monoisotopic mass table.


import sys
#Local aligner

#uhhh okay okay.
#str1=input()
#str2=input()

class Matrix:
    def __init__(self, string1, string2):
        '''form matrix of nodes and calculate score for each node'''
        self.nodelist=[[0 for x in range(len(string1)+1)] for y in range(len(string2)+1)]
        #initialize as list of lists
        self.seq1=string1
        self.seq2=string2
        list1=list(string1)
        list2=list(string2)
        for y in range(1,len(string2)+1):
            self.nodelist[y][0]= self.nodelist[(y-1)][0]-2
            #set the first row to be zero (since we can freely skip any distance of the prefix)
        for y in range(1,len(string2)+1):
            for x in range(1,len(string1)+1):
                vertical=-2+self[x,(y-1)]
                horizontal=-2+self[(x-1),y]
                if list1[(x-1)]==list2[(y-1)]:
                    diagonal=1+self[(x-1), (y-1)]
                else:
                    diagonal=-2+self[(x-1),(y-1)]
                score=max(vertical, horizontal, diagonal)
                self.nodelist[y][x]=score
    def __str__(self):
        '''a convenience method so we can see what the grid looks like. slow on large grids'''
        string=''
        for i in self.nodelist:
            string+=str(i)+'\n'
        return string
    def __getitem__(self, i):
        '''a convenience method letting us index with (x,y) tuple'''
        x=i[0]
        y=i[1]
        return self.nodelist[y][x]
    def calculate_max(self):
        '''find the max score and its index'''
        max_x=len(self.seq1)
        max_y=len(self.seq2)
        rows_of_interest=[((max_x,index), self[-1,y]) for index, y in enumerate(range(max_y+1))]
        max_score=max(rows_of_interest, key=lambda x: x[1])
        return max_score
    def backtrace(self):
        '''perform the backtracing'''
        x_prime=[]
        y_prime=[]
        max_score= self.calculate_max()
        x,y=max_score[0]
        max_score=max_score[1]
        while x*y !=0:
            if self[(x-1),(y-1)]+1 ==self[x,y] and self.seq1[x-1]==self.seq2[y-1]:
                x_prime.append(self.seq1[x-1])
                y_prime.append(self.seq2[y-1])
                x-=1
                y-=1
            elif self[(x-1), (y-1)]-2 == self[x,y] and self.seq1[x-1] != self.seq2[y-1]:
                x_prime.append(self.seq1[x-1])
                y_prime.append(self.seq2[y-1])
                y-=1
                x-=1
            elif self[(x, (y-1))]-2==self[x,y]:
                x_prime.append("-")
                y_prime.append(self.seq2[y-1])
                y-=1
            else:
                y_prime.append("-")
                x_prime.append(self.seq1[x-1])
                x-=1
        fh=open("answer.txt", "w")
        fh.write(str(max_score))
        fh.write("\n")
        fh.write(''.join(x_prime[::-1]))
        fh.write("\n")
        fh.write(''.join(y_prime[::-1]))
        fh.write("\n")
if __name__=="__main__":
    filename=sys.argv[1]
    header_with_seq={}
    with open(filename, "r") as f:
        for line in f:
            if line[0]==">":
                #if this is a header line, set it as dict key
                header=line.strip()[1:]
                header_with_seq[header]=""
            else:
                header_with_seq[header]+=line.strip().upper()
            #add sequence as value under header key
    seqs=list(header_with_seq.values())
    string1=seqs[0]
    string2=seqs[1]
    string1=string1.replace("\n",'')
    string2=string2.replace("\n",'')
    print(string1)
    print("\n"*2)
    print(string2)
    m=Matrix(string1, string2)
    m.backtrace()
