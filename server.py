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

    ### Get new user and goal info from form user input on homepage
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
    
    doc_ref = db.collection(u'users').document(u'{}'.format(username))
    doc_ref.set(user_dict) ### Add user to db
    ### TODO - this route is currently overriding the same user document each time

    goal_dict = {
        u'goal': goal,
        u'goal-completion': goal_completion,
        u'username': username,
    }

    doc_ref = db.collection(u'goals').document(u'{}'.format(goal))
    doc_ref.set(goal_dict) ### Add user's goal to db

    return(f"{email} successfully written to db. <<{goal}>> successfully written.")


@app.route('/view-users')
def show_users():
    """View all users written to Firestone -- for production only"""

    users_ref = db.collection(u'users')
    docs = users_ref.get()
    docs_list = []

    for doc in docs:
        docs_list.append(f'{doc.to_dict()}') 

    return jsonify(docs_list)


@app.route('/view-goals')
def show_goals():
    """View all goals written to Firestone -- for production only"""

    goals_ref = db.collection(u'goals')
    docs = goals_ref.get()
    docs_list = []

    for doc in docs:
        docs_list.append(f'{doc.to_dict()}') 

    return jsonify(docs_list)


@app.route('/refresh-collections')
def refresh_collections():
    """Delete all collections from Firestore-- for use in development only"""

    users_ref = db.collection(u'users')
    user_docs = users_ref.get()
    goals_ref = db.collection(u'goals')
    goal_docs = goals_ref.get()

    docs_list = []

    for doc in user_docs:
        docs_list.append(f'{doc.to_dict()}') 
        doc.reference.delete()

    for doc in goal_docs:
        docs_list.append(f'{doc.to_dict()}')
        doc.reference.delete()

    return jsonify(docs_list)


# @app.route('/get-goal', methods=['GET'])
# def retrieve_goal():

#     doc_ref = db.collection(u'sampleGoals').document(u'goal1')

#     try:
#         doc = doc_ref.get()
#         print(u'Document data: {}'.format(doc.to_dict()))

#     except google.cloud.exceptions.NotFound:
#         print(u'No such document!')



##### Dunder-Main ##########################################################

if __name__ == "__main__":
    
    ### debug must be True at time DebugToolbarExtension invoked
    app.debug = True
    
    ### ensures templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    ### enables use of DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')