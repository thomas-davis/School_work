import requests
import random
res=requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain")
#a list of several thousand plain text words
res=res.text.split()
word=(random.choice(res))
word=list(word.lower())
#our word to be guessed, randomly chosen from the website
wordxlist=["X" for i in word] 
guessedletter=[]
n=0
while n < 10:
	print("Your word is:", ''.join(wordxlist))
	guess=input("Guess a Letter: ")
	guessedletter.append(guess)
	if guess in word:
		print('yes')
		a=[k for k in enumerate(word)]
		foundletter=list(filter(lambda x:x[1]==guess, a))
#returns tuple (position of found letter, foundletter)
		for i,k in foundletter: 
			wordxlist[i]=k
		if wordxlist==word:
			break 	
	else:	
		n+=1
		print("No\n you've used", ''.join(guessedletter),'and have', 10-n, 'lives left')
if 10-n > 0:
	print("you won!")
else: 
	print("you lose! your word was", ''.join(word))
