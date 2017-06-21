
from flask import Flask, jsonify, abort, make_response, render_template
app = Flask(__name__)
app.config.from_object("config")