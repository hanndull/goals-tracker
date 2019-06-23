import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, flash, session, jsonify
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
#from model import db, User, Goal ### TODO-- this import line is now causing errors

##### Firebase #############################################################

cred = credentials.Certificate("firebase-key.json")
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

##### Create App #############################################################

app = Flask(__name__)

app.secret_key = 'HannahJohnson' ### Only for use during development 

### Raise an error for an undefined variable in Jinja
app.jinja_env.undefined = StrictUndefined

##### Define Routes ##########################################################

@app.route('/')
def show_homepage():

    return render_template('homepage.html')


@app.route('/add-user')
def add_user():

    ### Get new user and goal info from form user input
    username = request.args.get('username')
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')
    goal = request.args.get('goal')
    goal_completion = request.args.get('goal-completion')


    user_dict = {
        u'username': username,
        u'name': name,
        u'email': email,
        u'password': password,
    }

    ### Add user to db

    doc_ref = db.collection(u'users').document(u'{}'.format(username))
    doc_ref.set(user_dict) 


    # response = getGoal() ### Need to connect this 
    # goal = response.body['goal']
    # user = response.body['user']

    # doc_ref = db.collection(u'sampleGoals').document(u'goal1')
    # doc_ref.set({
    #     u'goal': goal,
    #     u'user': user,
    # })

    return(f"{email} successfully written to db.")

    ### Sets goal and user in db. Goal and user can be retrieved in JS??


@app.route('/view-users')
def show_users():

    pass

@app.route('/get-goal', methods=['GET'])
def retrieve_goal():

    doc_ref = db.collection(u'sampleGoals').document(u'goal1')

    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))

    except google.cloud.exceptions.NotFound:
        print(u'No such document!')



##### Dunder-Main ##########################################################

if __name__ == "__main__":
    
    ### debug must be True at time DebugToolbarExtension invoked
    app.debug = True
    
    ### ensures templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    ### enables use of DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')