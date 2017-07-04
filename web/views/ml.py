# coding: utf-8

from flask  import Flask,request,session,g,redirect,url_for,Blueprint
from flask import abort,render_template,flash
from helpers import getAvatar
#from .base import BaseHandler
import os
import time
import cPickle
import datetime
import logging
import werkzeug
import optparse
import numpy as np
import pandas as pd
from PIL import Image
import cStringIO as StringIO
import urllib
#import exifutil
import config
config = config.rec()

ml = Blueprint('ml', __name__)
import pika

REPO_DIRNAME = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../uploads')
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpe', 'jpeg', 'gif'])


#class LoginHandler(BaseHandler):
@ml.route('/login', methods=['GET', 'POST'])
def login():
    return redirect("/user/login")
 

@ml.route('/')
def index():
    return render_template('ml_index.html', has_result=False)


@ml.route('/classify_url', methods=['GET'])
def classify_url():
    imageurl = request.args.get('imageurl', '')
    try:
        string_buffer = StringIO.StringIO(
            urllib.urlopen(imageurl).read())
        image = caffe.io.load_image(string_buffer)

    except Exception as err:
        # For any exception we encounter in reading the image, we will just
        # not continue.
        logging.info('URL Image open error: %s', err)
        return render_template(
            'index.html', has_result=True,
            result=(False, 'Cannot open image from URL.')
        )

    logging.info('Image: %s', imageurl)
    result = app.clf.classify_image(image)
    return render_template(
        'index.html', has_result=False, result=result, imagesrc=imageurl)


@ml.route('/classify_upload', methods=['POST'])
def classify_upload():
    print 1111
    try:
        # We will save the file to disk for possible data collection.
        imagefile = request.files['imagefile']
        filename_ = str(time.time()).replace('[ |:]', '_') + \
            werkzeug.secure_filename(imagefile.filename)
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        print filename
        imagefile.save(filename)
        logging.info('Saving to %s.', filename)
        #image = exifutil.open_oriented_im(filename)
        image = Image.open(filename)

    except Exception as err:
        print 'Uploaded image open error: %s' % err
        return render_template(
            'ml_index.html', has_result=False,
            result=(False, 'Cannot open uploaded image.')
        )

    #result = app.clf.classify_image(image)
    return render_template(
        'ml_index.html', has_result=False, result=None
    )

 