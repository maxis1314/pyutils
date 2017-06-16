# coding: utf-8

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash,session
from tools.MysqlBase import *
import hashlib
import feedparser

mysql = MysqlBase('python')

rss_view = Blueprint('rss', __name__)


@rss_view.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':       
        feed = feedparser.parse('http://feed.cnblogs.com/blog/u/161528/rss')        
        return render_template('rss/index.html',feeds = feed['items'],active='rss')
        
    if request.method == 'POST':        
        return redirect(url_for('todos.show'))

