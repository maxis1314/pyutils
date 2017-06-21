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


FEED_FIELDS = {
    "id": fields.Integer,
    "url": fields.String,
    "flag": fields.Integer,
} 

class FeedList(Resource):
    '''
    this is Task list resource
    '''
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("url", type=unicode,
                                   required=True, help="No task name provided", location="json")
        self.reqparse.add_argument("flag", type=int, required=True, location="json")
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
        return {"tasks": [marshal(feed, FEED_FIELDS) for feed in feeds]}

    def post(self):
        '''
        method to add a task
        '''
        args = self.reqparse.parse_args()         
        feed = models.Feed(args["url"], args["flag"])

        db.session.add(feed)
        db.session.commit()

        return {"task": marshal(feed, TASK_FIELDS)}, 201


 
api.add_resource(FeedList,
                 "/api/v1.0/feeds",
                 endpoint="ep_notes")
