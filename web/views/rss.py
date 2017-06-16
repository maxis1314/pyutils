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


@rss_view.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':       
        feeds = mysql.query_h('select * from rss order by dt desc')     
        return render_template('rss/index.html',feeds = feeds,active='rss')
        
    if request.method == 'POST':        
        return redirect(url_for('todos.show'))
        
@rss_view.route('/sync')
def sync():
    mysql.execute('delete from rss')
    feeds = mysql.query_h('select * from feed')     
    for url in feeds:
        feed = feedparser.parse(url['url']) 
        for item in feed['items']:
            mysql.insert('insert ignore into rss(dt,link,title,body) values(%s,%s,%s,%s)',(item.get('date'),item.get('link'), item.get('title'), item.get('summary')))
    return redirect(url_for('rss.index'))