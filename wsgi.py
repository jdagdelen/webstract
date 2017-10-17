#from main import application
from app import dashapp

# standard Dash css, fork this for a custom theme
dashapp.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == "__main__":
    # application.run()
    dashapp.run_server()
