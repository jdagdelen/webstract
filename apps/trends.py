from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from plotly.graph_objs import Histogram
import pandas as pd
import tqdm
import pickle
import operator
from app import dashapp, cache
from apps.search import search_for_material


def generate_trends_graph(search='', material=''):
    if search is None:
        search = ''
    if material is None:
        material = ''
    print("searching for '{}'".format(material))
    results = search_for_material(material=material, search=search)

    if len(results) > 0:
        histdata = {}
        years = [r["year"] for r in results]
        for year in years:
            if year in histdata.keys():
                histdata[year] += 1
            else:
                histdata[year] = 1
        for year in range(min(2000, min(histdata.keys())), max(histdata.keys())):
            if not year in histdata.keys():
                histdata[year] = 0
        histdata = sorted(histdata.items(), key=operator.itemgetter(0))
        hist = {
            'data': [
                {
                    'x': [x[0] for x in histdata],
                    'y': [x[1] for x in histdata],
                    'name': 'Hist 1',
                    'type': 'scatter',
                    'marker': {'size': 12}
                }]}
    else:
        hist = {
            'data': [
                {
                    'x': [],
                    'y': [],
                    'name': 'Hist 1',
                    'type': 'scatter',
                    'marker': {'size': 12}
                }]}
    return hist

figure = generate_trends_graph(material="graphene")

# The Trends app
layout = html.Div([
    html.Div([
        html.Div([
            html.P('Matstract Trends: materials mentions over time.')
        ], style={'margin-left': '10px'}),
        # html.Label('Search the database:'),
        # dcc.Textarea(id='trends-search-box',
        #              cols=100,
        #              autoFocus=True,
        #              spellCheck=True,
        #              wrap=True,
        #              placeholder='Paste abstract/other text here to extract materials mentions.'
        #              ),
        # dcc.Dropdown(id='trends-dropdown',
        #              multi=True,
        #              placeholder='Material: e.g. "LiFePO4"',
        #              value=[],
        #              # options=[{'label': i, 'value': i} for i in df['NAME'].tolist()]),
        #              options=[]),
        dcc.Input(id='trends-material-box',
                  placeholder='Material: e.g. "graphene"',
                  value='',
                  type='text'),
        dcc.Input(id='trends-search-box',
                  placeholder='optional search criteria',
                  type='text'),
        html.Button('Submit', id='trends-button'),
        html.Div([
            html.Label("Number of papers mentioning {} per year".format("Graphene"), id="graph-label"),
            dcc.Graph(id='trend', figure=figure)]),
    ], className='twelve columns'),
])


@dashapp.callback(
    Output('trend', 'figure'),
    # [Input('search-box', 'value')])
    [Input('trends-button', 'n_clicks')],
    [State('trends-material-box', 'value'), State('trends-search-box', 'value')])
def update_graph(n_clicks, material, search):
    figure = generate_trends_graph(search=search, material=material)
    figure["mode"] = "histogram"
    return figure

@dashapp.callback(
    Output('graph-label', 'children'),
    [Input('trends-button', 'n_clicks')],
    [State('trends-material-box', 'value'), State('trends-search-box', 'value')])
def update_title(n_clicks, material, search):
    if len(search) == 0:
        return "Number of papers mentioning {} per year:".format(material)
    else:
        if len(material) > 0:
            return "Number of papers related to '{}' mentioning {} per year:".format(search, material)

    return ''


