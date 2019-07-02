
import bs4 
import requests
from time import sleep
def newpuzzle(): 
 res=requests.get('http://puzzlemaker.discoveryeducation.com/code/BuildWordSearch.asp') 
 res.raise_for_status()
 soup=bs4.BeautifulSoup(res.text)
 table=soup.select('center')
 finaltable=str(table[0])
 finaltable=finaltable[8:471].lower()
 finaltable=finaltable.replace(' ','') 
 sleep(1) 
 return finaltable
