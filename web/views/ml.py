# coding: utf-8

from flask  import Flask,request,session,g,redirect,url_for,Blueprint
from flask import abort,render_template,flash
from helpers import getAvatar
import config
#from .base import BaseHandler
import base
config = config.rec()

ml = Blueprint('ml', __name__)
import pika

#class LoginHandler(BaseHandler):
@ml.route('/login', methods=['GET', 'POST'])
def login():
    return redirect("/user/login")
 

