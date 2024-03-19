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

def get_all_admins():
    return db.session.query(Admin).all()

def get_all_admins_json():
    admins = get_all_admins()
    if not admins:
        return []
    admins = [admin.get_json() for admin in admins]
    return admins

# delete other users

# edit other users