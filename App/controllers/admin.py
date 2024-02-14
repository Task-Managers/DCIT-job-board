from App.models import User, Admin
from App.database import db

# create and add a new admin into the db
def add_admin(username, password, email):
        newAdmin= Admin(username, password, email)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newAdmin)
            db.session.commit()  # Commit to save the new to the database
            return newAdmin
        except:
            db.session.rollback()
            return None



# delete other users

# edit other users