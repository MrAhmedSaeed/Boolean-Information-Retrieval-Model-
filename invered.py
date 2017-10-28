import numpy as np
from nltk.tokenize import word_tokenize
# Quran Data set
file = "Quran Translation.txt"
file = open(file, "r")
data1 = file.readlines()
#Stop words
file2 = "Stopword-List.txt"
file2 = open(file2, "r")
SW = file2.readlines()


a=1
hadeeths=[]
#Hadeeths Dataset
for i in range(1,16):
    file =str(a)
    file = open(file, "r")
    data = file.readlines()
    hadeeths.append(data)
    a=a+1


stopwords=[]
#Remove \n from stop word
for i in SW:
    i=i.replace("\n","")
    stopwords.append(i)

verse_no=[]
verse_text=[]
verse=""
#READ document ID/Text and store in different lists 
for i in range(0,len(data1)):
    text=data1[i]
    if(text[:1]!='['):
        text = text.translate(str.maketrans('','','1234567890'))
        verse+=text
    if(text[:1]=='['):
        text=text.replace("\n","")
        verse_no.append(text)
        if(i!=0):
            verse_text.append(verse)
        verse=""
    if(i==len(data1)-1):
        verse_text.append(verse)

hadeeth=""
for i in range(0,len(hadeeths)):
    for j in range(0,len(hadeeths[i])):
        text=hadeeths[i][j]
        if(text[:1]!='['):
           text = text.translate(str.maketrans('','','1234567890'))
           hadeeth+=text
        if(text[:1]=='['):
            text=text.replace("\n","")
            verse_no.append(text)
            if(j!=0):
                verse_text.append(hadeeth)
            hadeeth=""
        if(j==len(data)-1):
            verse_text.append(hadeeth)
#*******************************************************************//

dictionary = {}
i=0
#Invered Index
for docID in verse_no:
        verse_text[i]=verse_text[i].translate(str.maketrans('','','!"#$%&\'()*+,-./:;<=>?@\^_`{|}~'))
        tokens = word_tokenize(verse_text[i].lower())
        for term in tokens:
            if (term not in dictionary):
                dictionary[term] = [docID]
            else:
                if (dictionary[term][-1] != docID):
                    dictionary[term].append(docID)
        i=i+1
#********************************************************************//
        
inverted_dictionary={}  
#Remove Stopword indexes from dictionary
for i in dictionary.keys():
    if(i not in stopwords and len(i)>2):
        inverted_dictionary[i]=dictionary[i]

import pickle
pickle.dump(inverted_dictionary, open( "inverted_index.p", "wb" ) )
    

