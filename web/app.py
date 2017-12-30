import dash
import flask
from flask_caching import Cache

dashapp = dashapp = dash.Dash()
server = dashapp.server
dashapp.title("Matstract: Materials Extraction from Abstracts")

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

if __name__ == '__main__':
    dashapp.run_server()
