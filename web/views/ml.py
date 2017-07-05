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
from tools.ML import *
#import exifutil
import config
config = config.rec()

ml = Blueprint('ml', __name__)
import pika

REPO_DIRNAME = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../static/uploads')
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpe', 'jpeg', 'gif'])

@ml.route('/')
def index():
    imag = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../tensorflow/use/cat.jpg')
    return render_template('ml_index.html', has_result=True,result = predict(imag))


@ml.route('/classify_url', methods=['GET'])
def classify_url():    
    imageurl = request.args.get('imageurl', UPLOAD_FOLDER)
    filename_ = str(time.time()).replace('[ |:]', '_') 
    filename = os.path.join(UPLOAD_FOLDER, filename_)+'.jpg'
    urllib.urlretrieve(imageurl,filename)
    return render_template(
        'ml_index.html', has_result=True, result=predict(filename), imagesrc=imageurl)


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
        print filename_
        imagefile.save(filename)
        logging.info('Saving to %s.', filename)
        #image = exifutil.open_oriented_im(filename)
        #image = Image.open(filename)

    except Exception as err:
        print 'Uploaded image open error: %s' % err
        return render_template(
            'ml_index.html', has_result=False,
            result=(False, 'Cannot open uploaded image.')
        )

    #result = app.clf.classify_image(image)
    return render_template(
        'ml_index.html', has_result=True, result=predict(filename),imagesrc=u'/static/uploads/'+filename_
    )

 