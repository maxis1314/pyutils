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
from tools.CrawlerBase import *

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

def sync_rss2():
    db = MysqlBase('python')
    crawler = CrawlerBase()
    title,content = crawler.get_rss('http://www.itpub.net/talk/',u'<div class="t1"><a href="([^"]*)" target="_blank" >([^<]*)</a></div>',u'<div class="r" id="[^"]*">([^<]*)')
    print 'num=',len(title)  
    print content
    for i in range(0,len(title)): 
        body = content[i]
        body=re.sub('<[^>]*?>','',body)
        db.insert('insert ignore into rss(dt,link,title,body) values(%s,%s,%s,%s)',('',title[i][0], title[i][1], body))
        
    title,content = crawler.get_rss('http://www.itpub.net/talk/index.php?m=it&page=2',u'<div class="t1"><a href="([^"]*)" target="_blank" >([^<]*)</a></div>',u'<div class="r" id="[^"]*">([^<]*)')
    print 'num=',len(title)  
    print content
    for i in range(0,len(title)): 
        body = content[i]
        body=re.sub('<[^>]*?>','',body)
        db.insert('insert ignore into rss(dt,link,title,body) values(%s,%s,%s,%s)',('',title[i][0], title[i][1], body))

        
def sync_rss(no, interval):
    db = MysqlBase('python')
    db.execute('update feed set flag=0') 
    db.execute('update rss set flag=1') 
    feeds = db.query_h('select * from feed')   
    sync_rss2()    
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
    status = int(request.args.get('status', 0))
    if status != 0:
        status = 1
    if request.method == 'GET':       
        feeds = mysql.query_h('select * from rss where flag=%d order by id desc limit 100'%status)     
        return render_template('rss/index.html',feeds = feeds,active='rss', status=status)        
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