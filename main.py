from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"

def get_number_of_abstracts():
    # do stuff
    return



