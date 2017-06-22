'''
all the REST api implementations
'''

import os
import uuid
import json

import werkzeug
from flask import abort, make_response, send_from_directory
from flask_restful import Api, Resource, reqparse, fields, marshal

from apps import app,models
from apps.models import db


api = Api(app)  # pylint: disable=C0103

@api.representation("application/json")
def output_json(data, code, headers=None):
    '''
    convert the response data to json
    '''
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

@api.representation("application/xml")
def output_xml(data, code, headers=None):
    '''
    convert the response data to xml
    TODO: place holder to implement xml response
    '''
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

TAG_FIELDS = {
    "id": fields.Integer,
    "name": fields.String,
}

FEED_FIELDS = {
    "id": fields.Integer,
    "url": fields.String,
    "flag": fields.Integer,
    "tags": fields.List(fields.Nested(TAG_FIELDS))
} 

class FeedList(Resource):
    '''
    this is Task list resource
    '''
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("url", type=unicode,
                                   required=True, help="No task url provided", location="form")
        self.reqparse.add_argument("flag", type=int, required=True, location="form")
        super(FeedList, self).__init__()

        self.representations = {
            "application/xml": output_xml,
            "application/json": output_json,
        }

    def get(self):
        '''
        method to get task list
        '''
        feeds = models.Feed.query.all()
        return {"feeds": [marshal(feed, FEED_FIELDS) for feed in feeds]}

    def post(self):
        '''
        method to add a task
        '''
        args = self.reqparse.parse_args()         
        feed = models.Feed(args["url"], args["flag"])

        db.session.add(feed)
        db.session.commit()

        return {"feed": marshal(feed, FEED_FIELDS)}, 201
        
    
class Feed(Resource):
    def get(self, feed_id):
        '''
        method to get task info by task id
        '''
        task = models.Feed.query.filter_by(id=feed_id).first()

        if not task:
            abort(404)

        return {"feed": marshal(task, FEED_FIELDS)}
    def delete(self, feed_id):
        '''
        method to delete task by task id
        '''
        feed = models.Feed.query.filter_by(id=feed_id).first()
        if not feed:
            abort(404)

        db.session.delete(feed)
        db.session.commit()
        return {"feed": feed.id}
 
api.add_resource(FeedList,
                 "/api/v1.0/feeds",
                 endpoint="ep_feeds")
api.add_resource(Feed,
                 "/api/v1.0/feed/<int:feed_id>",
                 endpoint="ep_feed")