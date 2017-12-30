from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

from web.app import dashapp, cache
from matstract import open_db_connection

db = open_db_connection()


def highlight_material(body, material):
    highlighted_phrase = html.Mark(material)
    if len(material) > 0 and material in body:
        chopped = body.split(material)
        newtext = []
        for piece in chopped[:-1]:
            newtext.append(piece)
            newtext.append(highlighted_phrase)
        newtext.append(chopped[-1])
        return newtext
    return body


def highlight_multiple_materials(body, materials):
    if len(materials) > 0 and any([material in body for material in materials]):
        newtext = []
        for material in materials:
            highlighted_phrase = html.Mark(material)
            if len(newtext) > 0:
                for body in newtext:
                    if type(body) == 'string' and len(material) > 0 and material in body:
                        chopped = body.split(material)
                        newnewtext = []
                        i = newtext.index(body)
                        for piece in chopped[:-1]:
                            newnewtext.append(piece)
                            newnewtext.append(highlighted_phrase)
                        newnewtext.append(chopped[-1])
                        newtext[i:i + 1] = newnewtext
            else:
                if len(material) > 0 and material in body:
                    chopped = body.split(material)
                    for piece in chopped[:-1]:
                        newtext.append(piece)
                        newtext.append(highlighted_phrase)
                    newtext.append(chopped[-1])
        return newtext
    return body


@cache.memoize(timeout=600)
def get_search_results(search="", material="", max_results=10000):
    if material is None:
        material = ''
    if search is None:
        search = ''
    if search == '' and material == '':
        return None
    if len(material) > 0:
        if material not in search:
            search = search + ' ' + material
            # print("searching for {}".format(search))
        results = db.abstracts.find({"$text": {"$search": search}, "chem_mentions.names": material},
                                    {"score": {"$meta": "textScore"}},
                                    ).sort([('score', {'$meta': 'textScore'})]).limit(max_results)
    else:
        results = db.abstracts.find({"$text": {"$search": search}}, {"score": {"$meta": "textScore"}},
                                    ).sort([('score', {'$meta': 'textScore'})]).limit(max_results)
    return list(results)


def generate_table(search='', materials='', columns=('title', 'authors', 'year', 'abstract'), max_rows=100):
    results = get_search_results(search, materials)
    # num_results = results.count()
    df = pd.DataFrame(results[0:100]) if results else pd.DataFrame()
    if not df.empty:
        format_authors = lambda author_list: ", ".join(author_list)
        df['authors'] = df['authors'].apply(format_authors)
        if len(materials.split(' ')) > 0:
            hm = highlight_material
        else:
            hm = highlight_material
        return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in columns])] +
            # Body
            [html.Tr([
                html.Td(html.A(hm(str(df.iloc[i][col]), materials),
                               href=df.iloc[i]["html_link"])) if col == "title"
                else html.Td(hm(str(df.iloc[i][col]), materials)) if col == "abstract"
                else html.Td(df.iloc[i][col]) for col in columns])
                for i in range(min(len(df), max_rows))]
        )
    return html.Table("No Results")


@cache.memoize(timeout=600)
def search_for_material(material, search):
    if search:
        results = db.abstracts.find({"$text": {"$search": search}, "chem_mentions.names": material}, ["year"])
    else:
        results = db.abstracts.find({"chem_mentions.names": material}, ["year"])
    return list(results)


# The Search app
layout = html.Div([
    html.Div([
        html.Div([
            html.P('Welcome to the Matstract Database!')
        ], style={'margin-left': '10px'}),

        html.Label('Search the database:'),
        dcc.Textarea(id='search-box',
                     cols=100,
                     autoFocus=True,
                     spellCheck=True,
                     wrap=True,
                     placeholder='Search: e.g. "Li-ion battery"'), ]),
    html.Div([
        dcc.Input(id='material-box',
                  placeholder='Material: e.g. "LiFePO4"',
                  type='text'),
        html.Button('Submit', id='search-button'),
    ]),
    # Row 2:
    html.Div([

        html.Div([

        ], className='nine columns', style=dict(textAlign='center')),

    ], className='row'),

    html.Div([
        html.Label('Top 100 Results:', id='number_results'),
        html.Table(generate_table(''), id='table-element')
    ], className='row')
])


@dashapp.callback(
    Output('table-element', 'children'),
    # [Input('search-box', 'value')])
    [Input('search-button', 'n_clicks')],
    [State('search-box', 'value'), State('material-box', 'value')])
def update_table(n_clicks, search, material):
    if not material is None:
        table = generate_table(search, material)
    else:
        table = generate_table(search)
    return table


@dashapp.callback(
    Output('number_results', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('search-box', 'value'), State('material-box', 'value')])
def update_num_results_label(n_clicks, search, material):
    results = get_search_results(search, material)
    if material or search:
        n = len(results)
        if n == 0:
            return "No Results"
        elif n == 10000:
            n = "> 10,000"
        return 'Showing {} of {} results'.format(100, n)
    else:
        return ''
