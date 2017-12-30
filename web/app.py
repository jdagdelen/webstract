import dash
from flask_caching import Cache
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from web.apps import search, trends, extract, similar

dashapp = dash.Dash()
server = dashapp.server

# dashapp = dash.Dash()
dashapp.config['suppress_callback_exceptions'] = True
cache = Cache(dashapp.server, config={"CACHE_TYPE": "simple"})

dashapp.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
BACKGROUND = 'rgb(230, 230, 230)'
COLORSCALE = [[0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
              [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"]]

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://s3-us-west-1.amazonaws.com/webstract/webstract.css"]

for css in external_css:
    dashapp.css.append_css({"external_url": css})


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
        return search.layout

if __name__ == '__main__':
    dashapp.run_server()
