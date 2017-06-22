'''
Models used in Remember
'''
from flask_sqlalchemy import SQLAlchemy

from apps import app
db = SQLAlchemy(app)    # pylint: disable=C0103


feed_tag = db.Table(  # pylint: disable=C0103
    "feed_tag",
    db.Column("feed_id", db.Integer, db.ForeignKey("feed.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"))
)

class Feed(db.Model):
    '''
    this is Task model
    '''
    id = db.Column(db.Integer, primary_key=True)    # pylint: disable=C0103
    url = db.Column(db.String(100))    
    flag = db.Column(db.Integer)
    tags = db.relationship("Tags")
    tags2 = db.relationship("Tags",secondary=feed_tag)
    
    def __init__(self, url, flag): # pylint: disable=too-many-arguments
        self.url = url
        self.flag = flag

    def __repr__(self):
        return "<Feed %r>" % self.url
class Tags(db.Model):
    '''
    this is Task model
    '''
    id = db.Column(db.Integer, primary_key=True)    # pylint: disable=C0103
    name = db.Column(db.String(100))    
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    
    def __init__(self, name, feed_id): # pylint: disable=too-many-arguments
        self.name = name
        self.feed_id = feed_id

    def __repr__(self):
        return "<Tags %r>" % self.url