import json
import os

from flask import Flask
from pymongo import MongoClient

application = Flask(__name__)

db_creds_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'db.json')
with open (db_creds_filename) as f:
    db_creds = json.load(f)
mongo_client = MongoClient(
    "mongodb://{user}:{pass}@{host}:{port}/{db}".format(**db_creds),
    connect=False)
db = mongo_client[db_creds["db"]]

@application.route("/")
def hello():
    return "Hello World! This is a test of pushing."

@application.route("/nabstracts")
def nabstracts():
    return "{} abstracts".format(db.abstracts.count())
