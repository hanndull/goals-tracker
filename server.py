import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, jsonify
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from passlib.hash import sha256_crypt 
    ###recommended from https://pythonprogramming.net/password-hashing-flask-tutorial/

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
    """Render the homepage template"""

    return render_template('homepage.html')


@app.route('/add-user')
def add_user():
    """Route that adds new goals and users.
    If username already exists, checks against stored encypted password. 
    """

    ### Get user and goal info from form user input on homepage
    username = request.args.get('username')
    entered_password = request.args.get('password')
    goal = request.args.get('goal')
    goal_completion = request.args.get('goal-completion')

    encrypted_password = sha256_crypt.encrypt(entered_password)
    ### encrypt pw for db, using using SHA256 as the algorithm

    user_dict = {
        u'username': username,
        u'password': encrypted_password,
    }

    doc_ref = db.collection(u'users').document(f'{username}')

    try:
        doc = doc_ref.get()
        dict_doc = doc.to_dict()

        if dict_doc == None:
            user_ref = db.collection(u'users').document(f'{username}') 
            user_ref.set(user_dict) ### Add new user to db  
       
        else:
            verification = sha256_crypt.verify(entered_password, dict_doc['password'])
            
            if verification == False:
                return('''Goal not saved.  
                    Please double check your password, and try again.''')
            
            elif verification == True:
                ### If verified, continues to goal creation
                print ('>>>>>>>>>>> PASSWORD SUCCESS')

    except google.cloud.exceptions.NotFound:
        
        print(u'No such document!')
        
        return('''Goal not saved. 
            Looks like there has been some sort of error. 
            Please try again later.''')
   
    goal_dict = {
        u'goal': goal,
        u'goalcompletion': goal_completion,
        u'username': username,
    }

    goal_ref = db.collection(u'goals').document(u'{}'.format(goal))
    goal_ref.set(goal_dict) ### Add user's new goal to db

    return('Your goal was successfully added.')


@app.route('/mygoals')
def render_mygoals():
    """Render template w/ form that allows user to check saved goals"""

    return render_template('mygoals.html')


@app.route('/check-goals')
def check_user_goals():
    """Validate user sign in info, and return user goals"""

    username = request.args.get('username')
    entered_password = request.args.get('password')

    encrypted_password = sha256_crypt.encrypt(entered_password)
    ### encrypt pw for db, using using SHA256 as the algorithm

    doc_ref = db.collection(u'users').document(f'{username}')

    doc = doc_ref.get()
    dict_doc = doc.to_dict()

    if dict_doc == None:
        return('''You have no saved goals. 
            Please create an account and save one 
            <a href='/'>here</a>.''')
   
    else:
        verification = sha256_crypt.verify(entered_password, dict_doc['password'])
        
        if verification == False:
            return('''Please double check your username and password, 
                    and try again.''')
        
        elif verification == True:
            
            goals_ref = db.collection(u'goals')
            docs_query = goals_ref.where(u'username', u'==', f'{username}')
            docs = docs_query.get()
            
            goals_list = []

            for doc in docs:
                goal_info ={
                    "goal": doc.get('goal'),
                    "goalcompletion": doc.get('goalcompletion'),
                }
                goals_list.append(goal_info)

            return jsonify(goals_list)


@app.route('/view-users')
def show_users():
    """View all users written to Firestone -- **for development only**"""

    users_ref = db.collection(u'users')
    docs = users_ref.get()
    docs_list = []

    for doc in docs:
        docs_list.append(f'{doc.to_dict()}') 

    return jsonify(docs_list)


@app.route('/view-goals')
def show_goals():
    """View all goals written to Firestone -- **for development only**"""

    goals_ref = db.collection(u'goals')
    docs = goals_ref.get()
    docs_list = []

    for doc in docs:
        docs_list.append(f'{doc.to_dict()}') 

    return jsonify(docs_list)


@app.route('/refresh-collections')
def refresh_collections():
    """Delete all collections from Firestore-- **for development only**"""

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


##### Dunder-Main ##########################################################

if __name__ == "__main__":
    
    ### debug must be True at time DebugToolbarExtension invoked
    app.debug = True
    
    ### ensures templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    ### enables use of DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')