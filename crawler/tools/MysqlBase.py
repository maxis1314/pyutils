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
sys.setdefaultencoding('utf8')

class MysqlBase:
    def __init__(self):
        self.conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306)
        cur=self.conn.cursor()
     
        #cur.execute('create database if not exists python')
        self.conn.select_db('python')
        #cur.execute('create table if not exists test(id int,info varchar(20))')
         
        value=[3,'hi rollen']
        cur.execute('insert into test values(%s,%s)',value)       
        self.conn.commit()
        cur.close()
    def insert(self,sql,value):
        values=[]
        values.append(value)
        self.multi_insert(sql,values)
        
    def multi_insert(self,sql,values):
        cur=self.conn.cursor()
        cur.executemany(sql,values)
        self.conn.commit()
        cur.close()
        
    def multi_insert_test(self):    
        values=[]
        for i in range(20):
            values.append((i,'hi rollen'+str(i)))
             
        self.multi_insert('insert into test values(%s,%s)',values)    
       
   

                            
