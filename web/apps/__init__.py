
from flask import Flask, jsonify, abort, make_response, render_template
app = Flask(__name__)
app.config.from_object("config")

app.template_folder = "../templates"
app.static_folder = "../static"