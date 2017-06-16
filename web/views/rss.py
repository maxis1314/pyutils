# coding: utf-8

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash,session,json
from tools.MysqlBase import *
import hashlib
import feedparser

mysql = MysqlBase('python')

rss_view = Blueprint('rss', __name__)
import re 
import time
import thread  
def timer(no, interval):  
    cnt = 0  
    while cnt<10:  
        print 'Thread:(%d) Time:%s %d\n'%(no, time.ctime(),cnt)  
        time.sleep(interval)  
        cnt+=1  
    thread.exit_thread()  

def sync_rss(no, interval):
    db = MysqlBase('python')
    db.execute('update feed set flag=0') 
    feeds = db.query_h('select * from feed')    
    for url in feeds:
        print url
        feed = feedparser.parse(url['url']) 
        print 'num=',len(feed['items'])
        print feed['items'][0]
        db.execute('update feed set flag=1 where id=%d'%url['id']) 
        for item in feed['items']: 
            body = item.get('summary')
            body=re.sub('<[^>]*?>','',body)
            db.insert('insert ignore into rss(dt,link,title,body) values(%s,%s,%s,%s)',(item.get('published'),item.get('link'), item.get('title'), body))
    thread.exit_thread()
    
@rss_view.route('/donerss')   
def donerss():    
    donecnt = mysql.query_h("""select count(*) as num,sum(flag) as done from feed""") 
    done= int(donecnt[0]['done'])
    return json.dumps({'num':donecnt[0]['num'],'done':done})    

@rss_view.route('/index', methods=['GET', 'POST'])
def index():
    #thread.start_new_thread(timer, (1,1)) 
    if request.method == 'GET':       
        feeds = mysql.query_h('select * from rss order by id desc limit 100')     
        return render_template('rss/index.html',feeds = feeds,active='rss')        
    if request.method == 'POST':
        _key = request.form['key']
        print _key
        feeds = mysql.query_h('select * from rss where title like \'%'+_key+u'%\' or body like \'%'+_key+u'%\' order by id desc limit 100')     
        return render_template('rss/index.html',feeds = feeds,key=_key)
        
@rss_view.route('/sync')
def sync():
    #mysql.execute('delete from rss')
    thread.start_new_thread(sync_rss, (1,1)) 
    return redirect(url_for('rss.index'))