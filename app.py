# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from pymongo import MongoClient
import json
import ast

dashapp = dash.Dash()

dashapp.layout = html.Div(children=[
    html.H1(children='Matstract DB'),

    html.Div(children='''
        Welcom to the Materials Abstract Database.
    '''),

    html.Div(dcc.Input(id='input-box', type="text", )),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children="""Enter Query [e.g. {"author":"Soren Tsarpinski"}]""")
])

def open_db_connection():

    db_creds_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'db.json')
    with open(db_creds_filename) as f:
        db_creds = json.load(f)
    mongo_client = MongoClient(
        "mongodb://{user}:{pass}@{host}:{port}/{db}".format(**db_creds),
        connect=False)
    db = mongo_client[db_creds["db"]]

    return db

@dashapp.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    db = open_db_connection()
    entries = db.abstracts.find(ast.literal_eval(value))
    count = entries.count()
    return "There are {:,} entries in the matstract database that meet that query.".format(count)

if __name__ == '__main__':
    dashapp.run_server(debug=True)