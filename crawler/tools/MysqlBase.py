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
    def __init__(self,dbname):
        self.conn=None
        self.reconn=False
        self.dbname=dbname
        self.connect()
    def connect(self):
        print '===========connect to database=============='
        if self.conn is not None:
            self.conn.close()
        self.conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306)        
        self.conn.select_db(self.dbname)
        self.conn.set_character_set('utf8')
        
    def reconnect(self):
        if self.reconn:
            self.connect()
    
    def execute(self,sql):
        try:
            self.reconnect()
            cur=self.conn.cursor()
            cur.execute(sql)       
            self.conn.commit()
            cur.close()
        except Exception,e:
            print 'db failed, reason:%s' % str(e)
            return None
    def query(self,sql,value=None):
        self.reconnect()
        cur=self.conn.cursor()
        if value is None:
            cur.execute(sql)
        else:
            cur.execute(sql,value)
        alldata = cur.fetchall()
        cur.close()
        return alldata
    def insert(self,sql,value):        
        values=[]
        values.append(value)
        self.multi_insert(sql,values)
        
    def multi_insert(self,sql,values):
        try:
            self.reconnect()
            cur=self.conn.cursor()
            cur.executemany(sql,values)
            self.conn.commit()
            cur.close()
        except Exception,e:
            print 'db failed, reason:%s' % str(e)
            return None
        
    def multi_insert_test(self):    
        values=[]
        for i in range(20):
            values.append((i,'hi rollen'+str(i)))
             
        self.multi_insert('insert into test values(%s,%s)',values)    
       
   

                            
