#Some code below patterned after 
    #https://github.com/GoogleCloudPlatform/python-docs-samples/blob/f13dcb36d25cd66f332830daeb9bacbc5ddb4ed9/firestore/cloud-client/snippets.py#L162-L176

from firebase_admin import firestore
from server import default_app

db = firestore.client()

class User(object):

    def __init__(self, username, name, email, password, goal_count=0):
        """Instanciate a user document/object"""

        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.goal_count = goal_count

    def from_dict(source):
        """Parse user info from dict"""
        user = User(
            source[u'username'], source[u'name'], 
            source[u'email'], source[u'password']
            )

        return user

    def to_dict(self):
        """Return all user info as dict"""

        user_dict = {
            u'username': self.username,
            u'name': self.name,
            u'email': self.email,
            u'password': self.password,
        }

        return user_dict

    def add_to_collection(self):
        """Add User to Firestore db"""

        doc_ref = db.collection(u'users').document(u'{}'.format(self.username))
        doc_ref.set(self.to_dict())   
            

    def check_password(self, input_password):
        """check to see if user password os correct"""

        try:
            self.password == input_password ### TODO - Fix this 

        except:
            pass    ### TODO - Fix this 


    def retrieve_collection():
        
        users_ref = db.collection(u'users')
        docs = users_ref.get()

        for doc in docs:
            print (f'{doc.id} => {doc.to_dict()}') 
            ### TODO - check if I need to change from "f" to u + format str

    def __repr__(self):
        """Display info on user"""

        return(
            f'''<{self.name} has username {self.username}. 
            Their email = {self.email}.>'''
            )


class Goal(object):

    def __init__(self, text, username, date):
        """Instantiate a goal document/object"""

        self.text = text
        self.username = username
        self.date = date



    def __repr__(self):
        """Diplay info on goal"""

        return(
            f'''<{self.username} created goal "{self.text}" on {self.date}.>
            '''
            )


def add_test_data():

    users_ref = db.collection(u'users')
    users_ref.document(u'HJ').set(
        User(u'hanno', u'Hannah Johnson', u'h@h.h', u'1234').to_dict())
