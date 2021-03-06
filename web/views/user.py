# coding: utf-8

from flask  import Flask,request,session,g,redirect,url_for,Blueprint
from flask import abort,render_template,flash
from helpers import getAvatar
import config
#from .base import BaseHandler
import base
config = config.rec()

user = Blueprint('user', __name__)
import pika

#class LoginHandler(BaseHandler):
@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if base.isAdmin():
            return redirect("/")
        else:
            return render_template("login.html",getAvatar=getAvatar)
    
    username = request.form['username']
    password = request.form['password']
    #connection = pika.BlockingConnection(pika.ConnectionParameters(
    #    host='localhost'))
    #channel = connection.channel()
    #channel.queue_declare(queue='hello')
    #channel.basic_publish(exchange='',
    #                      routing_key='hello',
    #                      body=u'u:'+username+' p:'+password)
    #print(" [x] Sent 'RABBITQUEUE'")
    #connection.close()

    if base.userAuth(username, password):
        flash('You were successfully logged in')
        base.currentUserSet(username)
        return redirect("/posts/")
    else:
        flash('User name or password error','error')
        return redirect("/user/login")

#class LogoutHandler(BaseHandler):
@user.route('/logout')
def logout():
    session.pop('user',None)
    flash('You were successfully logged out')
    return redirect('/user/login')

