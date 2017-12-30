from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import dashapp
from apps import extract, search, trends, similar

# Header and Intro text
header = html.Div([
    dcc.Location(id="url", refresh=False),
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
    html.Nav(
        style={
            'position': 'relative',
            'top': '0px',
            'left': '27px',
            'cursor': 'default'
        },
        children=[
            dcc.Link("Search", href="/search", ),
            html.Span(' • '),
            dcc.Link("Trends", href="/trends"),
            html.Span(' • '),
            dcc.Link("Extract", href="/extract"),
            html.Span(' • '),
            dcc.Link("Similar Abstracts", href="/similar")
        ],
        id="nav_bar"),
    html.Br()
], className='row twelve columns', style={'position': 'relative', 'right': '15px'})


dashapp.layout = html.Div([header, html.Div(search.layout, id='page-content')],
                          className='container')


@dashapp.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(path):
    if path == "/search":
        return search.layout
    elif path == "/trends":
        return trends.layout
    elif path == "/extract":
        return extract.layout
    elif path == "/similar":
        return similar.layout
    else:
        return '404'


if __name__ == '__main__':
    dashapp.run_server(debug=True)
