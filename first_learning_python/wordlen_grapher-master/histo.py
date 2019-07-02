import plotly.plotly as py
import plotly.graph_objs as go
from collections import defaultdict

def histo(string):
 """takes string, returns dict of wordlength vs percent frequency"""
 string=stripper(string)
 liststring=string.split()
 lens=list(map(len,liststring))
 #at this point we have a list of the lengths of each word
 counts=counter(lens)
 return counts

def counter(a): 
 """takes list of word lengths, gives frequency of each length"""
 counts=defaultdict(int) 
 for length in a: 
  counts[length]+=1 
 return counts

def stripper(a):
 """the pattented grammer stripper 3000. Takes out the grammar from the string"""
 chars=['"','(',')','.','?','!',';','-','--',',',':'] 
 for i in chars: 
  a=a.replace(i,'') 
 return a

def makehisto(*args):
 """take variable numbers of strings, use histo to make a list of dicts of wordlength vs frequency, then converts that to a bar graph with plotly"""
 titles=(input('what are the titles, in order: ')) 
 titles=titles.split()
 wordlendicts=[] 
 for i in args: 
  wordlendicts.append(histo(i))
 data=[]
 kys=[]
 vls=[] 
 for i in wordlendicts: 
  kys.append(list(i.keys())) 
  vls.append(list(i.values()))
 for n,(k,v) in enumerate(zip(kys,vls)): 
  data.append(go.Bar(x=k,y=v,name=titles[n])) 
 layout=go.Layout(barmode='group',
 yaxis=dict(title='percent frequency of occurence'),
 xaxis=dict(title='length of word'))
 fig=go.Figure(data=data,layout=layout) 
 py.plot(fig,filename=str(titles))
