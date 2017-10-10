from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World! This is a test of pushing."

def get_number_of_abstracts():
    # do stuff
    return



