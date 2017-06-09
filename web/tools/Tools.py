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
reload(sys)  
import jieba
sys.setdefaultencoding('utf8')

def lineProcess(line):
    list1 = list(jieba.cut(line, cut_all=False))
    list1 = filter(f, list1)
    return list1

def f(x): 
    if x=='\n' or x=='\t' or x==' ' or x=='，' or len(x)<=1 or len(x)>=8:
        return False       
    
    match = re.search('^[0-9a-zA-Z\.\-_#]+$', x)    
    if match:
        return False
    return True
def savetofile(filename,summer):
    with open(filename, 'w') as f:                     # open file with write-mode
        picklestring = pickle.dump(summer, f)   # serialize and save object
def loadtovar(filename):
    with open(filename, 'r') as f:
        summer = pickle.load(f)   # read file and build object
    return summer