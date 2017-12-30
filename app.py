from web.app import dashapp

server = dashapp.server

if __name__ == '__main__':
    dashapp.run_server(debug=True)