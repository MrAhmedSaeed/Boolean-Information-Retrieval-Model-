# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 16:32:59 2017

@author: Ahmed
"""
import pickle
inverted_index = pickle.load( open( "inverted_index.p", "rb" ) )
Positional_index = pickle.load( open( "Positional_index.p", "rb" ))
#Quran document data set for showing Result*/
file = "Quran Translation.txt"
file = open(file, "r")
#******************************************/
#STOPWORD file for remove stopwords from documents*/
file2 = "Stopword-List.txt"
file2 = open(file2, "r")
#******************************************/
#READ Quran data set
data1 = file.readlines()
#READ Stopwords
SW = file2.readlines()

verse_no=[]
verse_text=[]
a=1
hadeeths=[]
#READ Hadeeths data set
for i in range(1,16):
    file =str(a)
    file = open(file, "r")
    data = file.readlines()
    hadeeths.append(data)
    a=a+1
#**********************/
stopwords=[]
# remove \n from stopword
for i in SW:
    i=i.replace("\n","")
    stopwords.append(i)

#READ document ID/Text and store in different lists 
verse=""
for i in range(0,len(data1)):
    text=data1[i]
    if(text[:1]!='['):
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
#******************************************************/

# AND with word POSTION in document 
def A_Posinal(TDocIds,dis):
    ANDresult={}
    DocIdsL=[val for val in TDocIds[0].keys() if val in TDocIds[1].keys()]
    for id in DocIdsL:
        listA = TDocIds[0][id]
        listB = TDocIds[1][id]
            
        for i in range(0,len(listA)):
            for j in range(0,len(listB)):
                if(abs(listA[i]-listB[j])<=dis+1):
                    if(id not in ANDresult.keys()):
                        ANDresult[id]=listB    
    return ANDresult

# Simple AND     
def A_Simple(TDocIds):
    A=TDocIds.pop()
    B=TDocIds.pop()
    DocIdsL=[val for val in A if val in B]
    
    return DocIdsL    

# Simple OR    
def OR_Simple(TDocIds):
    A=TDocIds.pop()
    B=TDocIds.pop()     
    DocIdsL=A+B
  
    return DocIdsL 
#SEARCH ENGINE FOR PROCESS QUERY****/        
def Search_Engine(q):
    query=q.lower()
    query=query.split();
    DocIds=[]
    AND_check=False
    OR_check=False
    # if query is not proximity
    if('/' not in q):    
        for i in range(0,len(query)):
            if('/' in query[i]):
                continue
            if(query[i]!='and' and query[i]!='or'):
                DocIds.append(inverted_index[query[i]])
                if(AND_check==True and len(DocIds)>1):
                    result=A_Simple(DocIds)
                    DocIds=[]
                    DocIds.append(result)
                    AND_check=False
                if(OR_check==True and len(DocIds)>1):
                    result=OR_Simple(DocIds)
                    DocIds=[]
                    DocIds.append(result)
                    OR_check=False
                    
            else:
                if(query[i]=='and'):
                    AND_check=True
                elif(query[i]=='or'):
                    OR_check=True
      
        Result=[]
         
        for i in range(0,len(verse_no)):
            for j in range(0,len(DocIds[0])):
                if(verse_no[i]==DocIds[0][j]):
                    Result.append((verse_no[i],verse_text[i]))
        
        return Result  
#if query is proximity             
    elif('/' in q):
        for i in range(0,len(query)):
            if('/' in query[i]):
                continue
            if(query[i]!='and' and query[i]!='or'):
                DocIds.append(Positional_index[query[i]])
                if(AND_check==True and len(DocIds)>1):
                    if( (i + 1 < len(query)) and '/' in query[i+1]):
                        distance=query[i+1]
                        result=A_Posinal(DocIds,int(distance[1:]))
                        DocIds=[]
                        DocIds.append(result)
                        print(DocIds)
                        AND_check=False
                    else:
                        result=A_Simple(DocIds)
                        DocIds.append(result)
                elif(OR_check==True and len(DocIds)>1):
                    result=OR_Simple(DocIds)
                    DocIds=[]
                    DocIds.append(result) 
                    OR_check=False
                    
            else:
                if(query[i]=='and'):
                    AND_check=True 
                elif(query[i]=='or'):
                    OR_check=True
                
        
        
        Result=[]
        
        print(DocIds[0].keys())      
        for i in range(0,len(verse_no)):
            if(verse_no[i] in DocIds[0].keys()):
                Result.append((verse_no[i],verse_text[i]))
                
        
    return Result
#END SEARCH ENGINE****************************************//

    
#.............................******GUI******........................................#

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from tkinter import *
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'ENTER YOUR QUERY'
        self.left = 400
        self.top = 300
        self.width = 400
        self.height = 140
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,30)
 
        # Create a button in the window
        self.button = QPushButton('Search', self)
        self.button.move(20,80)
 
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        result=Search_Engine(self.textbox.text())
        va='/**************************************************************************Retrieved Documents********************************************************\n Totoal Retrieved Documents:'+str(len(result))+'\n \n'
        for Did,text in result:
            va+=str(Did)+' '+text+'\n'
            
        
        pass

        root = Tk()
        text = Text(root,width=150,height=30)
        text.insert(INSERT, va)
        
        text.pack()
        
        
        
        root.mainloop()   
        
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
    
    
    

















