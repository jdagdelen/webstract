import json
import os

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from pymongo import MongoClient


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

application = Flask(__name__)

db_creds_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'db.json')
with open (db_creds_filename) as f:
    db_creds = json.load(f)
mongo_client = MongoClient(
    "mongodb://{user}:{pass}@{host}:{port}/{db}".format(**db_creds),
    connect=False)
db = mongo_client[db_creds["db"]]

# @application.route("/")
# def hello():
#     return "Hello World! This is another a test of pushing."

# @application.route("/")
# def nabstracts():
#     return "There are currently {:,} abstracts in the Matstract Database".format(db.abstracts.count())

@application.route("/", methods=['GET', 'POST'])
def index(nabstracts=None):
	if request.method == 'POST':
		nabstracts = "{:,}".format(db.abstracts.count())
	render_template('index.html')



