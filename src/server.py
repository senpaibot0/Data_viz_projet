'''
    Contains the server to run our application.
'''
from flask_failsafe import failsafe

@failsafe
def create_app():
    '''
        Gets the underlying Flask server from our Dash app.
    '''
    from app import app  # pylint: disable=import-outside-toplevel
    return app.server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Port dynamique donné par Render
    create_app().run(host="0.0.0.0", port=port, debug=True)