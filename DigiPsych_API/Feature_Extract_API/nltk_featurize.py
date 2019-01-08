import nltk
from nltk import word_tokenize
#import speech_recognition as sr_audio
import numpy as np
from textblob import TextBlob
#import transcribe as ts

try:
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

def nltk_featurize(file):
    #Check if required resources are installed


	# get transcript
    if file[-4:]=='.wav':
        transcript=ts.transcribe_sphinx('test.wav')
    else:
        transcript=file
    #alphabetical features
    a=transcript.count('a')
    b=transcript.count('b')
    c=transcript.count('c')
    d=transcript.count('d')
    e=transcript.count('e')
    f=transcript.count('f')
    g_=transcript.count('g')
    h=transcript.count('h')
    i=transcript.count('i')
    j=transcript.count('j')
    k=transcript.count('k')
    l=transcript.count('l')
    m=transcript.count('m')
    n=transcript.count('n')
    o=transcript.count('o')
    p=transcript.count('p')
    q=transcript.count('q')
    r=transcript.count('r')
    s=transcript.count('s')
    t=transcript.count('t')
    u=transcript.count('u')
    v=transcript.count('v')
    w=transcript.count('w')
    x=transcript.count('x')
    y=transcript.count('y')
    z=transcript.count('z')
    space=transcript.count(' ')

    #numerical features and capital letters
    num1=transcript.count('0')+transcript.count('1')+transcript.count('2')+transcript.count('3')+transcript.count('4')+transcript.count('5')+transcript.count('6')+transcript.count('7')+transcript.count('8')+transcript.count('9')
    num2=transcript.count('zero')+transcript.count('one')+transcript.count('two')+transcript.count('three')+transcript.count('four')+transcript.count('five')+transcript.count('six')+transcript.count('seven')+transcript.count('eight')+transcript.count('nine')+transcript.count('ten')
    number=num1+num2
    capletter=sum(1 for c in transcript if c.isupper())

    #part of speech
    text=word_tokenize(transcript)
    g=nltk.pos_tag(transcript)
    cc=0
    cd=0
    dt=0
    ex=0
    in_=0
    jj=0
    jjr=0
    jjs=0
    ls=0
    md=0
    nn=0
    nnp=0
    nns=0
    pdt=0
    pos=0
    prp=0
    prp2=0
    rb=0
    rbr=0
    rbs=0
    rp=0
    to=0
    uh=0
    vb=0
    vbd=0
    vbg=0
    vbn=0
    vbp=0
    vbp=0
    vbz=0
    wdt=0
    wp=0
    wrb=0

    for i in range(len(g)):
    	if g[i][1] == 'CC':
    		cc=cc+1
    	elif g[i][1] == 'CD':
    		cd=cd+1
    	elif g[i][1] == 'DT':
    		dt=dt+1
    	elif g[i][1] == 'EX':
    		ex=ex+1
    	elif g[i][1] == 'IN':
    		in_=in_+1
    	elif g[i][1] == 'JJ':
    		jj=jj+1
    	elif g[i][1] == 'JJR':
    		jjr=jjr+1
    	elif g[i][1] == 'JJS':
    		jjs=jjs+1
    	elif g[i][1] == 'LS':
    		ls=ls+1
    	elif g[i][1] == 'MD':
    		md=md+1
    	elif g[i][1] == 'NN':
    		nn=nn+1
    	elif g[i][1] == 'NNP':
    		nnp=nnp+1
    	elif g[i][1] == 'NNS':
    		nns=nns+1
    	elif g[i][1] == 'PDT':
    		pdt=pdt+1
    	elif g[i][1] == 'POS':
    		pos=pos+1
    	elif g[i][1] == 'PRP':
    		prp=prp+1
    	elif g[i][1] == 'PRP$':
    		prp2=prp2+1
    	elif g[i][1] == 'RB':
    		rb=rb+1
    	elif g[i][1] == 'RBR':
    		rbr=rbr+1
    	elif g[i][1] == 'RBS':
    		rbs=rbs+1
    	elif g[i][1] == 'RP':
    		rp=rp+1
    	elif g[i][1] == 'TO':
    		to=to+1
    	elif g[i][1] == 'UH':
    		uh=uh+1
    	elif g[i][1] == 'VB':
    		vb=vb+1
    	elif g[i][1] == 'VBD':
    		vbd=vbd+1
    	elif g[i][1] == 'VBG':
    		vbg=vbg+1
    	elif g[i][1] == 'VBN':
    		vbn=vbn+1
    	elif g[i][1] == 'VBP':
    		vbp=vbp+1
    	elif g[i][1] == 'VBZ':
    		vbz=vbz+1
    	elif g[i][1] == 'WDT':
    		wdt=wdt+1
    	elif g[i][1] == 'WP':
    		wp=wp+1
    	elif g[i][1] == 'WRB':
    		wrb=wrb+1

    #sentiment
    tblob=TextBlob(transcript)
    polarity=float(tblob.sentiment[0])
    subjectivity=float(tblob.sentiment[1])

    #word repeats
    words=transcript.split()
    newlist=transcript.split()
    repeat=0
    for i in range(len(words)):
    	newlist.remove(words[i])
    	if words[i] in newlist:
    		repeat=repeat+1

    features=np.array([a,b,c,d,
    e,f,g_,h,
    i,j,k,l,
    m,n,o,p,
    q,r,s,t,
    u,v,w,x,
    y,z,space,number,
    capletter,cc,cd,dt,
    ex,in_,jj,jjr,
    jjs,ls,md,nn,
    nnp,nns,pdt,pos,
    prp,prp2,rbr,rbs,
    rp,to,uh,vb,
    vbd,vbg,vbn,vbp,
    vbz,wdt,wp,wrb,
    polarity,subjectivity,repeat])

    labels=['a', 'b', 'c', 'd',
    		'e','f','g','h',
    		'i', 'j', 'k', 'l',
    		'm','n','o', 'p',
    		'q','r','s','t',
    		'u','v','w','x',
    		'y','z','space', 'numbers',
    		'capletters','cc','cd','dt',
    		'ex','in','jj','jjr',
    		'jjs','ls','md','nn',
    		'nnp','nns','pdt','pos',
    		'prp','prp2','rbr','rbs',
    		'rp','to','uh','vb',
    		'vbd','vbg','vbn','vbp',
    		'vbz', 'wdt', 'wp','wrb',
    		'polarity', 'subjectivity','repeat']

    return features, labels
