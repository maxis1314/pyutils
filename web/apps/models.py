'''
Models used in Remember
'''
from flask_sqlalchemy import SQLAlchemy

from apps import app
db = SQLAlchemy(app)    # pylint: disable=C0103

class Feed(db.Model):
    '''
    this is Task model
    '''
    id = db.Column(db.Integer, primary_key=True)    # pylint: disable=C0103
    url = db.Column(db.String(100))    
    flag = db.Column(db.Integer)
    
    def __init__(self, url, flag): # pylint: disable=too-many-arguments
        self.url = url
        self.flag = flag

    def __repr__(self):
        return "<Task %r>" % self.url
