#-*- encoding:UTF-8 -*-
import os
import pickle
from Tools import *
from numpy import *
    
class Predict:
    def __init__(self):
        self.model = os.path.join(os.path.dirname(__file__),'../model/0.model')
        trainDirFiles,cateWordsProb, cateWordsNum,wordMapDict = loadtovar(os.path.join(os.path.dirname(__file__),'../model/0.model'))
        self.md5_cat = loadtovar(os.path.join(os.path.dirname(__file__),'../model/md5_catname'))
        self.trainDirFiles=trainDirFiles
        self.cateWordsProb=cateWordsProb
        self.cateWordsNum=cateWordsNum
        self.wordMapDict=wordMapDict
        
    def classify(self,str):
        testFilesWords=list(lineProcess(str))
        testFilesWords = filterWords(testFilesWords)
        #print testFilesWords
        
        #for i in sorted(cateWordsProb.items(), key=lambda d: d[1],reverse=True):
        #    print i[0],'\t',i[1]
        trainTotalNum = sum(self.cateWordsNum.values())
        for k in range(len(self.trainDirFiles)):
            p = self.computeCateProb(self.trainDirFiles[k], testFilesWords,\
                                self.cateWordsNum, trainTotalNum, self.cateWordsProb)
            #print self.trainDirFiles[k],'~',p
            if k==0:
                maxP = p
                bestCate = self.trainDirFiles[k]
                continue
            if p > maxP:
                maxP = p
                bestCate = self.trainDirFiles[k]
        return self.md5_cat[bestCate]
        
    def maybe(self,str,n):
        testFilesWords=list(lineProcess(str))
        testFilesWords = filterWords(testFilesWords)
        for x in testFilesWords:
            print x
        
        #for i in sorted(cateWordsProb.items(), key=lambda d: d[1],reverse=True):
        #    print i[0],'\t',i[1]
        trainTotalNum = sum(self.cateWordsNum.values())
        score={}
        for k in range(len(self.trainDirFiles)):
            p = self.computeCateProb(self.trainDirFiles[k], testFilesWords,\
                                self.cateWordsNum, trainTotalNum, self.cateWordsProb)
            #print self.trainDirFiles[k],'~',p
            score[self.trainDirFiles[k]]=p
        
        count=0
        possiblelabel = []
        for i in sorted(score.items(), key=lambda d: d[1],reverse=True):            
            possiblelabel.append(self.md5_cat[i[0]]) 
            count=count+1
            if count >= n:
                break
        return possiblelabel
        
    def computeCateProb(self,traindir,testFilesWords,cateWordsNum,\
                    totalWordsNum,cateWordsProb):
        prob = 0
        wordNumInCate = cateWordsNum[traindir]  # 类k下单词总数 <类目，单词总数>
        for i in range(len(testFilesWords)):
            keyName = traindir + '_' + testFilesWords[i]
            if cateWordsProb.has_key(keyName):
                testFileWordNumInCate = cateWordsProb[keyName] # 类k下词c出现的次数
            else: testFileWordNumInCate = 0.0
            xcProb = log((testFileWordNumInCate + 0.0001) / (wordNumInCate + totalWordsNum))  # 求对数避免很多很小的数相乘下溢出
                     
            prob = prob + xcProb
        res = prob + log(wordNumInCate) - log(totalWordsNum)
        return res
                       
    def filterWords(words):    
        newwords=[]
        for word in words:        
            if word in self.wordMapDict.keys():
                newwords.append(word)
        return newwords