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

@rss_view.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':       
        feeds = mysql.query_h('select * from rss order by id desc')     
        return render_template('rss/index.html',feeds = feeds,active='rss')        
    if request.method == 'POST':
        _key = request.form['key']
        print _key
        feeds = mysql.query_h('select * from rss where title like \'%'+_key+u'%\' or body like \'%'+_key+u'%\' order by id desc')     
        return render_template('rss/index.html',feeds = feeds,key=_key)
        
@rss_view.route('/sync')
def sync():
    #mysql.execute('delete from rss')
    feeds = mysql.query_h('select * from feed')     
    for url in feeds:
        print url
        feed = feedparser.parse(url['url'])         
        for item in feed['items']: 
            body = item.get('summary')
            body=re.sub('<[^>]*?>','',body)
            mysql.insert('insert ignore into rss(dt,link,title,body) values(%s,%s,%s,%s)',(item.get('published'),item.get('link'), item.get('title'), body))
    return redirect(url_for('rss.index'))