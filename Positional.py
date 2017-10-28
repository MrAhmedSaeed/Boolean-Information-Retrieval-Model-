# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 05:59:08 2017

@author: Ahmed
"""

from nltk.tokenize import word_tokenize
# Quran Data set
file = "Quran Translation.txt"
file = open(file, "r")
data1 = file.readlines()
#STOPWORDS
file2 = "Stopword-List.txt"
file2 = open(file2, "r")
SW = file2.readlines()


verse_no=[]
verse_text=[]
stopwords=[]
a=1
hadeeths=[]
#Hadeeths Data set
for i in range(1,16):
    file =str(a)
    file = open(file, "r")
    data = file.readlines()
    hadeeths.append(data)
    a=a+1
#Remove \n from stop word
for i in SW:
    i=i.replace("\n","")
    stopwords.append(i)


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
#*********************************************************************//


i=0
#input list of word and get with their postions in output
def index_one_file(DocWords):
	fileIndex = {}
	for index, word in enumerate(DocWords):
		if word in fileIndex.keys():
			fileIndex[word].append(index)
		else:
			fileIndex[word] = [index]
	return fileIndex
 
 
#input Doument Id with their words and get dictionary with positions of word in document
def make_indices(DocID_words):
	total = {}
	for filename in DocID_words.keys():
		total[filename] = index_one_file(DocID_words[filename])
	return total

#Final Positional Index
def fullIndex(regdex):
	total_index = {}
	for filename in regdex.keys():
		for word in regdex[filename].keys():
			if word in total_index.keys():
				if filename in total_index[word].keys():
					total_index[word][filename].extend(regdex[filename][word][:])
				else:
					total_index[word][filename] = regdex[filename][word]
			else:
				total_index[word] = {filename: regdex[filename][word]}
	return total_index


        
        
        
        

dictionary = {}
result={}
Final_Postional_index={}
Doc={}
i=0
for docID in verse_no:
        verse_text[i]=verse_text[i].translate(str.maketrans('','','!"#$%&\'()*+,-./:;<=>?@\^_`{|}~'))
        tokens = word_tokenize(verse_text[i].lower())
            
        Doc[docID]=tokens
        result=make_indices(Doc)
        Final_Postional_index=fullIndex(result)
        tokens=[]
        words=[]
        Ftokens=[]
        i=i+1

Positional_dictionary={}  
#Remove Stopword indexes from dictionary
for i in Final_Postional_index.keys():
    if(i not in stopwords and len(i)>2):
        Positional_dictionary[i]=Final_Postional_index[i]

import pickle
pickle.dump(Positional_dictionary, open( "Positional_index.p", "wb" ) )