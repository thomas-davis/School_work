#project to try to solve word searches
global counter
counter=0
import newpuzzle2
def wsbetter(wordstofind):
 global counter
 wordsearch=newpuzzle2.newpuzzle()
 for i in wordstofind:
  i=i.lower() 
  check(i,0,wordsearch)
 counter+=1
#feeds each word into checker one at a time
def check(wordtofind,offset, wordsearch):
 global counter
 if wordsearch.find(wordtofind,offset)>=0: 
  startpos=wordsearch.find(wordtofind,offset)
 #finds the first instance of the first letter of the word to find
 #this is our start position
  wordlen=len(wordtofind)
  checker={}
  up=[]
  down=[]
  downleft=[]
  upleft=[]
  upright=[]
  downright=[]
  try:
   checker['forward']=(wordsearch[startpos:(startpos+wordlen)])
   checker['backward']=(wordsearch[startpos:((startpos-wordlen)):-1])
#adds strings of length word to find to dict,
#before and after start position
   for i in range(wordlen):
    try:
     down.append(wordsearch[startpos+16*i])
     up.append(wordsearch[startpos-16*i])
     downright.append(wordsearch[startpos+17*i]) 
     downleft.append(wordsearch[startpos+15*i])
     upleft.append(wordsearch[startpos-17*i])
     upright.append(wordsearch[startpos-15*i])
     checker['up']=''.join(up)
     checker['down']=''.join(down)
     checker['down and right']=''.join(downright)
     checker['down and left']=''.join(downleft)
     checker['up and right']=''.join(upright)
     checker['up and left']=''.join(upleft)
    except IndexError: 
     pass
#example of what's in checker:
#{'down and right': 'gazyu', 'down and left': 'gfesy', 'up and right': 'gishf', 'up': 'gqiew', 'forward': 'great',
# 'down': 'gvrgu', 'up and left': 'gsioc', 'backward': 'gsovz'}
   checkervl=list(checker.values())
   wordfound=list(filter(lambda v: v==wordtofind, checkervl)) 
   assert(wordfound)
   position=list(divmod(startpos,16))
   directions=list(checker.keys())
   a=('\n %s found at column %s and row %s going %s in puzzle number %s \n%s') % (wordtofind,position[1]+1,position[0]+1, directions[(checkervl.index(wordfound[0]))], counter,wordsearch)
   with open('foundword.txt','a') as file:
    file.write(a)
  except AssertionError:
   startpos+=1
   check(wordtofind,startpos,wordsearch)
 else: 
  print(wordtofind,'not found')
#if we didn't find it, we try again with the next instance of the wordtofind's first letter   
