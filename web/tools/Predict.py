#-*- encoding:UTF-8 -*-
import urllib2
import re
import StringIO
import gzip
import logging
import sqlite3
import logutils
import urllib
import sys
import MySQLdb
from Tools import *
reload(sys)  
import jieba
sys.setdefaultencoding('utf8')

    
class Predict:
    def __init__(self,dbname):
        self.model = os.path.join(os.path.dirname(__file__),'../model/0.model')
        trainDirFiles,cateWordsProb, cateWordsNum = loadtovar(os.path.join(os.path.dirname(__file__),'../model/0.model'))
        self.md5_cat = loadtovar(os.path.join(os.path.dirname(__file__),'../model/md5_catname'))
        self.trainDirFiles=trainDirFiles
        self.cateWordsProb=cateWordsProb
        self.cateWordsNum=cateWordsNum
        
    def classify(str):
        testFilesWords=list(lineProcess(str))
        #print testFilesWords
        
        #for i in sorted(cateWordsProb.items(), key=lambda d: d[1],reverse=True):
        #    print i[0],'\t',i[1]
        trainTotalNum = sum(self.cateWordsNum.values())
        for k in range(len(self.trainDirFiles)):
            p = computeCateProb(self.trainDirFiles[k], testFilesWords,\
                                self.cateWordsNum, trainTotalNum, self.cateWordsProb)
            #print trainDirFiles[k],'~',p
            if k==0:
                maxP = p
                bestCate = trainDirFiles[k]
                continue
            if p > maxP:
                maxP = p
                bestCate = trainDirFiles[k]
        return self.md5_cat[bestCate]
        
    
                            
