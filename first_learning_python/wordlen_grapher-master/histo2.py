import plotly.plotly as py
import plotly.graph_objs as go
def prep(a): 
 """takes list of word lengths, gives frequency of each length"""
 counts={}
 totallen=(len(a))
 for i in a: 
  if i not in counts:
   counts[i]=0
  counts[i]+=(1/totallen) 
 return counts

def stripper(a):
 """the pattented grammer stripper 3000. Takes out the grammar from the string"""
 chars=['"','(',')','.','?','!',';','-','--',',',':'] 
 for i in chars: 
  a=a.replace(i,'') 
 return a

def histo(a):
 """takes string, returns dict of wordlength vs percent frequency"""
 a=stripper(a)
 a=a.split()
 lensA=list(map(lambda x:len(x),a))
 #at this point we have a list of the lengths of each word
 countsa=prep(lensA)
 return countsa
 
def makehisto(*args):
 """take variable numbers of strings, use histo to make a list of dicts of wordlength vs frequency, then converts that to a bar graph with plotly"""
 titles=(input('what are the titles, in order: ')) 
 titles=titles.split()
 c=[] 
 for i in args: 
  c.append(histo(i))
 data=[]
 kys=[]
 vls=[] 
 for i in c: 
  kys.append(list(i.keys())) 
  vls.append(list(i.values()))
 for n,(k,v) in enumerate(zip(kys,vls)): 
  data.append(go.Bar(x=k,y=v,name=titles[n])) 
 data=data
 layout=go.Layout(barmode='group',
 yaxis=dict(title='percent frequency of occurence'),
 xaxis=dict(title='length of word'))
 fig=go.Figure(data=data,layout=layout) 
 py.plot(fig,filename=str(titles))
