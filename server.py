import firebase_admin
from firebase_admin import credentials
from flask import Flask, render_template, request, flash, session, jsonify
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

##### Firebase #############################################################

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

##### Create App #############################################################

app = Flask(__name__)

app.secret_key = 'HannahJohnson' ### Only for use during development 

### Raise an error for an undefined variable in Jinja
app.jinja_env.undefined = StrictUndefined

##### Define Routes ##########################################################

@app.route('/')
def show_homepage():

    return render_template('homepage.html')

##### Dunder-Main ##########################################################

if __name__ == "__main__":
    
    ### debug must be True at time DebugToolbarExtension invoked
    app.debug = True
    
    ### ensures templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    ### enables use of DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')