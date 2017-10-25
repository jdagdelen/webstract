import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import flask
import os
import json
from pymongo import MongoClient

server = flask.Flask('matstract')
dashapp = dash.Dash('Matstract')

BACKGROUND = 'rgb(230, 230, 230)'

COLORSCALE = [ [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
                [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"] ]

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

# def make_query(query_string):
#     if query_string == "":
#         return [-1, pd.DataFrame()]
#     db = open_db_connection()
#     abstracts = db.abstracts
#     results = db.abstracts.find({"$text": {"$search": query_string}}, {"score": {"$meta": "textScore"}},
#                  ).sort([('score', {'$meta': 'textScore'})]).limit(100)
#     num_results = results.count()
#     df = pd.DataFrame(list(results))
#     if not df.empty:
#         return df[['title','authors', 'year', 'abstract']]
#     return [num_results, df]
#
# def generate_table(num_results, dataframe, selected_columns = ['title','authors', 'year', 'abstract'], max_rows=100):
#     if num_results == 0:
#         return html.Table("No results.")
#
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
#         # Body
#         [html.Tr([
#             html.Td(dataframe.iloc[i][col]) for col in selected_columns
#         ]) for i in range(min(len(dataframe), max_rows))]
#     )

def generate_table(search, columns = ['title','authors', 'year', 'abstract'], max_rows=100):
    if search.strip() == "":
        return html.Table()
    db = open_db_connection()
    results = db.abstracts.find({"$text": {"$search": search}}, {"score": {"$meta": "textScore"}},
                 ).sort([('score', {'$meta': 'textScore'})]).limit(100)
    num_results = results.count()
    df = pd.DataFrame(list(results))
    if not df.empty:
        format_authors = lambda author_list: ", ".join(author_list)
        df['authors'] = df['authors'].apply(format_authors)

        return html.Table(
                # Header
                [html.Tr([html.Th(col) for col in columns])] +

                # Body
                [html.Tr([
                    html.Td(df.iloc[i][col]) for col in columns
                ]) for i in range(min(len(df), max_rows))]
            )
    return html.Table("No Results")

dashapp.layout = html.Div([

    # Row 1: Header and Intro text

    html.Div([
        html.Img(src="https://s3-us-west-1.amazonaws.com/webstract/matstract_with_text.png",
                style={
                    'height': '100px',
                    'float': 'right',
                    'position': 'relative',
                    'bottom': '40px',
                    'left': '50px'
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
                      type='text')
            ], className='twelve columns' )

    ], className='row' ),


    # Row 2: Hover Panel and Graph

    html.Div([

        html.Div([

        ], className='nine columns', style=dict(textAlign='center')),


    ], className='row' ),

    html.Div([
        html.Label('Top 100 Results:'),
        html.Table(generate_table(''), id='table-element' )
    ])

], className='container')


# @dashapp.callback(
#     Output('table-element', 'children'),
#     [Input('title_dropdown', 'value')])
# def update_table(title_dropdown_value):
#     # print(title_dropdown_value)
#     table = make_dash_table(title_dropdown_value)
#     return table

@dashapp.callback(
    Output('table-element', 'children'),
    [Input('search-box', 'value')])
def update_table(search):
    # [nr, df] = make_query(search)
    # format_authors = lambda author_list: ", ".join(author_list)
    # if not df.empty:
    #     df['authors'] = df['authors'].apply(format_authors)
    table = generate_table(search)
    return table

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://s3-us-west-1.amazonaws.com/webstract/webstract.css"]

for css in external_css:
    dashapp.css.append_css({"external_url": css})

if __name__ == '__main__':
    dashapp.run_server()
