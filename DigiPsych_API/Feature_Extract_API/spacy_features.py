import spacy
from spacy.symbols import nsubj, VERB
from textblob import TextBlob
import numpy as np
import os
#Install Spacy library
    #Installation requires Visual C++ 14.0
    #If installation doesn't work - usually fail at ujson
        # get wheel at https://www.lfd.uci.edu/~gohlke/pythonlibs/#Ujson
        #pip install wheel at local directory
# To leverage spacy, also include this download
    #os.system("python -m spacy download en_core_web_sm")

def stats(matrix):
    mean=np.mean(matrix)
    std=np.std(matrix)
    maxv=np.amax(matrix)
    minv=np.amin(matrix)
    median=np.median(matrix)
    output=np.array([mean,std,maxv,minv,median])
    return output


def spacy_featurize(transcript):
    nlp=spacy.load('en_core_web_sm')
    doc=nlp(transcript)

    # initialize lists
    entity_types=['PERSON','NORP','FAC','ORG',
                  'GPE','LOC','PRODUCT','EVENT',
                  'WORK_OF_ART','LAW','LANGUAGE',
                  'DATE','TIME','PERCENT','MONEY',
                  'QUANTITY','ORDINAL','CARDINAL']

    pos_types=['PROPN', 'ADP', 'DET', 'NUM',
               'PUNCT', 'SPACE', 'VERB', 'NOUN',
               'ADV', 'CCONJ', 'PRON', 'ADJ',
               'SYM', 'PART', 'INTJ', 'X']

    tag_types=['NNP', 'IN', 'DT', 'CD',
               'NNPS', ',', '_SP', 'VBZ',
               'NN', 'RB', 'CC', '', 'NNS',
               '.', 'PRP', 'MD', 'VB',
               'HYPH', 'VBD', 'JJ', ':',
               '-LRB-', '$', '-RRB-', 'VBG',
               'VBN', 'NFP', 'RBR', 'POS',
               'VBP', 'RP', 'JJS', 'PRP$',
               'EX', 'JJR', 'WP', 'WDT',
               'TO', 'WRB', "''", '``',
               'PDT', 'AFX', 'RBS', 'UH',
               'WP$', 'FW', 'XX', 'SYM', 'LS',
               'ADD']

    dep_types=['compound', 'ROOT', 'prep', 'det',
               'pobj', 'nummod', 'punct', '',
               'nsubj', 'advmod', 'cc', 'conj',
               'aux', 'dobj', 'nmod', 'acl',
               'appos', 'npadvmod', 'amod', 'agent',
               'case', 'intj', 'prt', 'pcomp',
               'ccomp', 'attr', 'dep', 'acomp',
               'poss', 'auxpass', 'expl', 'mark',
               'nsubjpass', 'quantmod', 'advcl', 'relcl',
               'oprd', 'neg', 'xcomp', 'csubj',
               'predet', 'parataxis', 'dative', 'preconj',
               'csubjpass', 'meta']


    shape_types=['\ufeffXxx', 'Xxxxx', 'XXxxx', 'xx',
                 'X', 'Xxxx', 'Xxx', ',', '\n\n',
                 'xXxxx', 'xxx', 'xxxx', '\n',
                 '.', ' ', '-', 'xxx.xxxx.xxx', '\n\n\n',
                 ':', '\n    ', 'dddd', '[', '#', 'dd', ']',
                 'd', 'XXX-d', '*', 'XXXX',
                 'XX', 'XXX', '\n\n\n\n', 'Xx',
                 '\n\n\n    ', '--', '\n\n    ', '    ',
                 '   ', '  ', "'x", 'x',
                 'X.', 'xxx--', ';', 'Xxx.',
                 '(', ')', "'", '“', '”',
                 'Xx.', '!', "'xx", 'xx!--Xxx',
                 "x'xxxx", '?', '_', "x'x", "x'xx",
                 "Xxx'xxxx", 'Xxxxx--', 'xxxx--',
                 '--xxxx', 'X--', 'xx--', 'xxxx”--xxx',
                 'xxx--“xxxx', "Xxx'x", ';--',
                 'xxx--_xxx', "xxx'x", 'xxx!--xxxx', 'xxxx?--_Xxx',
                 "Xxxxx'x", 'xxxx--“xxxx', "xxxx'xxx", '--Xxxxx',
                 ',--', '?--', 'xx--“xx', 'xx!--X',
                 '.--', 'xxx--“xxx', ':--', 'Xxxxx--“xxxx',
                 'xxxx!--xxxx', 'xx”--xxx', 'xxxx--_xxx', 'xxxx--“xxx',
                 '--xx', '--X', 'xxxx!--Xxx', '--xxx',
                 'xxx_.', 'xxxx--_xx', 'xxxx--_xx_xxxx', 'xx!--xxxx',
                 'xxxx!--xx', "X'xx", "xxxx'x", "X_'x",
                 "xxx'xxx", '--Xxxx', "X'Xxxxx", "Xx'xxxx",
                 '--Xxx', 'xxxx”--xxxx', 'xxxx!--',
                 'xxxx--“x', 'Xxxx!--Xxxx', 'xxx!--Xxx', 'Xxxxx.',
                 'xxxx_.', 'xx--“Xxxx', '\n\n   ', 'Xxxxx”--xxx',
                 'xxxx”--xx', 'xxxx--“xx', "Xxxxx!--Xxx'x", "X'xxxx",
                 'Xxxxx?--', '--Xx', 'xxxx!”--Xx', "xxxx--“X'x", "xxxx'",
                 'xxx.--“Xxxx', 'xxxx--“X', 'xxxx!--X', 'Xxx”--xx', 'xxx”--xxx',
                 'xxx-_xxx', "x'Xxxxx", 'Xxxxx!--X', 'Xxxxx!--Xxx',
                 'dd-d.xxx', 'xxxx://xxx.xxxx.xxx/d/dd/', 'xXxxxx', 'xxxx://xxxx.xxx/xxxx',
                 'd.X.', '/', 'd.X.d', 'd.X',
                 '%', 'Xd', 'xxxx://xxx.xxxx.xxx', 'ddd(x)(d',
                 'X.X.', 'ddd', 'xxxx@xxxx.xxx', 'xxxx://xxxx.xxx',
                 '$', 'd,ddd']

    chunkdep_types=['ROOT', 'pobj', 'nsubj', 'dobj', 'conj',
                    'appos', 'attr', 'nsubjpass', 'dative', 'pcomp']

    # initialize lists
    features=list()
    labels=list()
    poslist=list()
    taglist=list()
    deplist=list()
    shapelist=list()
    sentences=list()
    sentence_length=0
    sent_polarity=list()
    sent_subjectivity=list()

    # EXTRACT ALL TOKENS
    for token in doc:
        if token.pos_ in pos_types:
            poslist.append(token.pos_)
        else:
            poslist.append('pos_other')
        if token.tag_ in tag_types:
            taglist.append(token.tag_)
        else:
            taglist.append('tag_other')
        if token.dep_ in dep_types:
            deplist.append(token.dep_)
        else:
            deplist.append('dep_other')
        if token.shape_ in shape_types:
            shapelist.append(token.shape_)
        else:
            shapelist.append('shape_other')

    pos_types.append('pos_other')
    tag_types.append('tag_other')
    dep_types.append('dep_other')
    shape_types.append('shape_other')

    # count unique instances throughout entire tokenization
    # keep labels as well
    for i in range(len(pos_types)):
        features.append(poslist.count(pos_types[i]))
        labels.append(pos_types[i])

    for i in range(len(tag_types)):
        features.append(taglist.count(tag_types[i]))
        labels.append(tag_types[i])

    for i in range(len(dep_types)):
        features.append(deplist.count(dep_types[i]))
        labels.append(dep_types[i])

    for i in range(len(shape_types)):
        features.append(shapelist.count(shape_types[i]))
        labels.append(shape_types[i])

    # EXTRACT SENTENCES
    for sent in doc.sents:
        sentences.append(sent.text)

    # NOW ITERATE OVER SENTENCES TO CALCULATE THINGS PER SENTENCE
    for i in range(len(sentences)):
        sent_polarity.append(TextBlob(sentences[i]).sentiment[0])
        sent_subjectivity.append(TextBlob(sentences[i]).sentiment[1])

    # STATISTICAL POLARITY AND SUBJECTIVITY FEATURES PER SENTENCE
    sent_polarity=stats(np.array(sent_polarity))
    for i in range(len(sent_polarity)):
        features.append(sent_polarity[i])
        if i == 0:
            labels.append('mean sentence polarity')
        elif i == 1:
            labels.append('std sentence polarity')
        elif i == 2:
            labels.append('max sentence polarity')
        elif i == 3:
            labels.append('min sentence polarity')
        elif i == 4:
            labels.append('median sentence polarity')

    sent_subjectivity=stats(np.array(sent_subjectivity))
    for i in range(len(sent_subjectivity)):
        features.append(sent_subjectivity[i])
        if i ==0:
            labels.append('mean sentence subjectivity')
        elif i==1:
            labels.append('std sentence subjectivity')
        elif i==2:
            labels.append('max sentence subjectivity')
        elif i==3:
            labels.append('min sentence subjectivity')
        elif i==4:
            labels.append('median sentence subjectivity')

    # CHARACTERS
    characters=len(transcript)
    features.append(characters)
    labels.append('character count')
    # TOTAL NUMBER OF WORDS
    words=len(transcript.split())
    features.append(words)
    labels.append('word count')
    # TOTAL NUMBER OF SENTENCES
    sentence_num=len(sentences)
    features.append(sentence_num)
    labels.append('sentence number')
    # WORDS PER SENTENCE
    wps=sentence_num/words
    features.append(wps)
    labels.append('words per sentence')

    # NEED TO GET MORE FEATURES
    #_________________________
    # EXTRACT NOUN CHUNKS
    chunktext=list()
    chunkroot=list()
    chunkdep=list()
    chunkhead=list()

    for chunk in doc.noun_chunks:
        if chunk.text not in chunk.text:
            chunktext.append(chunk.text)
            #print('text:'+chunk.text)
        if chunk.root.text not in chunkroot:
            chunkroot.append(chunk.root.text)
        # later extract chunkdep
        chunkdep.append(chunk.root.dep_)
        if chunk.root.head.text not in chunkhead:
            chunkhead.append(chunk.root.head.text)

    features.append(len(chunktext))
    labels.append('unique chunk noun text')
    features.append(len(chunkroot))
    labels.append('unique chunk root text')
    features.append(len(chunkhead))
    labels.append('unique chunk root head text')

    for i in range(len(chunkdep_types)):
        features.append(chunkdep.count(chunkdep_types[i]))
        labels.append('chunkdep '+chunkdep_types[i])

    # EXTRACT NAMED ENTITY FREQUENCIES
    ent_texts=list()
    ent_labels=list()

    for ent in doc.ents:
        ent_texts.append(ent.text)
        ent_labels.append(ent.label_)

    features.append(len(ent_texts))
    labels.append('number of named entities')

    for i in range(len(entity_types)):
        features.append(ent_labels.count(entity_types[i]))
        labels.append(entity_types[i])

    return features, labels
