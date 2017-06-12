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
reload(sys)  
sys.setdefaultencoding('utf8')


def dict_factory(cursor, row): 
  d = {} 
  for idx, col in enumerate(cursor.description): 
    d[col[0]] = row[idx] 
  return d
  
class SqliteBase:
    def __init__(self,name):
        self.name = name
        self.conn=None
        self.reconn=True
        self.connect()
        #init table         
        self.execute("create table if not exists info(id integer primary key,info varchar(100))")
        
    def connect(self):
        if self.conn is not None:
            self.conn.close()
        self.conn = sqlite3.connect(self.name)
        self.conn.row_factory = dict_factory
        
    def reconnect(self):
        if self.reconn:
            self.connect()
            
    def execute(self,sql):
        self.reconnect()
        cur=self.conn.cursor()
        cur.execute(sql)       
        self.conn.commit()
        cur.close()
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
    def query_h(self,sql,value=None):
        self.reconnect()
        cur=self.conn.cursor()
        if value is None:
            cur.execute(sql)
        else:
            cur.execute(sql,value)
        alldata = cur.fetchall()
        cur.close()
        return alldata


                            
