import dash
import flask
from flask_caching import Cache

server = flask.Flask(__name__)
dashapp = dash.Dash(__name__, server=server)
# dashapp = dash.Dash()
dashapp.config['suppress_callback_exceptions'] = True
cache = Cache(dashapp.server, config={"CACHE_TYPE": "simple"})

dashapp.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
BACKGROUND = 'rgb(230, 230, 230)'
COLORSCALE = [[0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
              [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"]]

# Function to make table of abstracts mentioning term

# @dashapp.callback(
#     Output('extract-number-results', 'children'),
#     [Input('extract-button', 'n_clicks')],
#     [State('extract-drowpdown', 'values')])
# def update_extract_table(n_clicks, materials):
#     if len(materials) > 0:
#         table = generate_abstracts_table()
#     if not material is None:
#         table = generate_table(search, material)
#     else:
#         table = generate_table(search)
#     return table

# Function to update number of returned abstracts in Extract app

# @dashapp.callback(
#     Output('extract-number-results', 'children'),
#     [Input('extract-button', 'n_clicks')],
#     [State('extract-drowpdown', 'values')])
# def update_num_results_label(n_clicks, materials):
#     results = get_entries_for_materials(materials)
#     if material or search:
#         n = len(results)
#         if n == 0:
#             return "No Results"
#         elif n == 10000:
#             n = "> 10,000"
#         return 'Showing {} of {} results'.format(100, n)
#     else:
#         return ''

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://s3-us-west-1.amazonaws.com/webstract/webstract.css"]

for css in external_css:
    dashapp.css.append_css({"external_url": css})

# if __name__ == '__main__':
#     dashapp.run_server()
