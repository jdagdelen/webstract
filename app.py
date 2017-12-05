import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import flask
import os
import json
from pymongo import MongoClient

server = flask.Flask(__name__)
dashapp = dash.Dash(__name__, server = server)

BACKGROUND = 'rgb(230, 230, 230)'

COLORSCALE = [ [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
                [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"] ]

def open_db_connection():

    # db_creds_filename = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)), 'db_atlas.json')
    # with open(db_creds_filename) as f:
    #     db_creds = json.load(f)

    db_creds = {"user":os.environ["ATLAS_USER"],
                "pass":os.environ["ATLAS_USER_PASSWORD"],
                "rest":os.environ["ATLAS_REST"],
                "db":"tri_abstracts"}

    uri = "mongodb://{user}:{pass}@{rest}".format(**db_creds)

    mongo_client = MongoClient(uri, connect=False)
    db = mongo_client[db_creds["db"]]
    return db

def generate_table(search, material='', columns = ['title','authors', 'year', 'abstract'], max_rows=100):
    if search.strip() == "":
        return html.Table()
    db = open_db_connection()
    if material not in search:
        search = material  + ' ' + search
    results = db.abstracts.find({"$text": {"$search": search + material}}, {"score": {"$meta": "textScore"}},
                 ).sort([('score', {'$meta': 'textScore'})]).limit(100)
    num_results = results.count()
    df = pd.DataFrame(list(results))
    if not df.empty:
        format_authors = lambda author_list: ", ".join(author_list)
        df['authors'] = df['authors'].apply(format_authors)
        # print([str(df.iloc[i][col]) + "as;ldkfjaspdlkfja;sldkfjas;dlfkj" for col in columns for i in range(min(len(df), max_rows))])
        return html.Table(
                # Header
                [html.Tr([html.Th(col) for col in columns])] +

                # Body
                [html.Tr([
                    html.Td(highlight_material(str(df.iloc[i][col]), material)) if
                    col == "abstract" or col == "title" else df.iloc[i][col] for col in columns
                    # html.Td(df.iloc[i][col]) for col in columns
                    # html.Mark(df.iloc[i][col]) for col in columns

        ]) for i in range(min(len(df), max_rows))]
            )
    return html.Table("No Results")

def highlight_material(body, material):
    highlighted_phrase = html.Mark(material)
    if material in body:
        chopped = body.split(material)
        newtext = []
        for piece in chopped:
            newtext.append(piece)
            newtext.append(highlighted_phrase)
        return  newtext
    return body

dashapp.layout = html.Div([

    # Row 1: Header and Intro text

    html.Div([
        html.Img(src="https://s3-us-west-1.amazonaws.com/webstract/matstract_with_text.png",
                style={
                    'height': '100px',
                    'float': 'right',
                    'position': 'relative',
                    'bottom': '20px',
                    'left': '10px'
                },
                ),
        html.H2('Matstract db',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '27px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '6.0rem',
                    'color': '#4D637F'
                }),
    ], className='row twelve columns', style={'position': 'relative', 'right': '15px'}),

    html.Div([
        html.Div([
            html.Div([
                html.P('Welcome to the Matstract Database!')
            ], style={'margin-left': '10px'}),

            html.Label('Search the database:'),
            dcc.Input(id='search-box',
                      value='',
                      type='text'),
            dcc.Input(id='material-box',
                      placeholder='Material: e.g. "LiFePO4"',
                      type='text'),
            html.Button('Submit', id='button'),
            ], className='twelve columns' )

    ], className='row' ),


    # Row 2:

    html.Div([

        html.Div([

        ], className='nine columns', style=dict(textAlign='center')),


    ], className='row' ),

    html.Div([
        html.Label('Top 100 Results:'),
        html.Table(generate_table(''), id='table-element' )
    ])

], className='container')

@dashapp.callback(
    Output('table-element', 'children'),
    # [Input('search-box', 'value')])
    [Input('button', 'n_clicks')],
    [State('search-box', 'value'), State('material-box', 'value')])
def update_table(n_clicks, search, material):
    table = generate_table(search, material)
    return table

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://s3-us-west-1.amazonaws.com/webstract/webstract.css"]

for css in external_css:
    dashapp.css.append_css({"external_url": css})

if __name__ == '__main__':
    dashapp.run_server()
