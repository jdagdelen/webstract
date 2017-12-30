from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from web.app import dashapp
from matstract import extract_materials


# The Extract App
layout = html.Div([
    html.Div([
        html.Div([
            html.P('Matstract Extract: materials extraction from text sources.')
        ], style={'margin-left': '10px'}),
        html.Label('Enter text for materials extraction:'),
        dcc.Textarea(id='extract-textarea',
                     cols=100,
                     autoFocus=True,
                     spellCheck=True,
                     wrap=True,
                     placeholder='Paste abstract/other text here to extract materials mentions.'
                     ),
        html.Div([html.Button('Extract Materials', id='extract-button')]),
        # dcc.Dropdown(id='extract-dropdown',
        #              multi=True,
        #              placeholder='Material: e.g. "LiFePO4"',
        #              # options=[{'label': i, 'value': i} for i in df['NAME'].tolist()]),
        #              ),
        dcc.Textarea(id='extract-results',
                     cols=100,
                     autoFocus=False,
                     wrap=True,
                     value="",
                     readOnly=True,
                     ),
        html.Div(id='extract-copy',
                 children=[])
        # dcc.Input(id='trends-material-box',
        #           placeholder='Material: e.g. "LiFePO4"',
        #           value='',
        #           type='text'),
        # dcc.Input(id='trends-search-box',
        #           placeholder='optional search criteria',
        #           type='text'),
        # html.Button('Submit', id='trends-button'),
        # dcc.Graph(id='trends', figure={}),
    ], className='twelve columns'),
])

@dashapp.callback(
    Output('extract-results', 'value'),
    [Input('extract-button', 'n_clicks')],
    [State('extract-textarea', 'value')])
def update_extract(n_clicks, text):
    if text is None:
        text = ''
    materials = extract_materials(text)
    materials = [m for m in materials if len(m) > 0]
    # return [{"name": m, "value": m} for m in materials]
    return ", ".join(materials)