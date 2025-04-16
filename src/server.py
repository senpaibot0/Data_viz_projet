'''
    Contains the server to run our application.
'''
from flask_failsafe import failsafe

from flask import Flask #app

app = Flask(__name__)

@app.route('/')
def create_app(*args, **kwargs):
    '''
        Gets the underlying Flask server from our Dash app.
    '''
    from app import app  # pylint: disable=import-outside-toplevel
    return app.server

if __name__ == "__main__":
    import os
    port = 9999
    print(f"✅ Starting server on port {port}")
    create_app().run(host="0.0.0.0", port=port, debug=False) #False
