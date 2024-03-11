from App.models import User, Alumni
from App.database import db

def add_alumni(username, password, email, alumni_id):
        newAlumni= Alumni(username, password, email, alumni_id)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newAlumni)
            db.session.commit()  # Commit to save the new  to the database
            return newAlumni
        except:
            db.session.rollback()
            return None

def get_all_alumni():
    return db.session.query(Alumni).all()

def get_alumni(alumni_id):
    return Alumni.query.filter_by(alumni_id=alumni_id).first()

def is_alumni_subscribed(alumni_id):
    alumni = get_alumni(alumni_id)

    if(alumni.subscribed == True):
        return True
    else:
        return False

def get_all_subscribed_alumni():
    all_alumni = Alumni.query.filter_by(subscribed=True)
    return all_alumni

# handle subscribing and unsubscribing
def subscribe_action(alumni_id, job_category=None):
    alumni = get_alumni(alumni_id)
    
    # if they are already susbcribed then unsubscribe them
    if is_alumni_subscribed(alumni_id):
        alumni.subscribed = False
    
    else:
        alumni.subscribed = True
        # set their jobs list to job_category ?

    db.session.add(alumni)
    return db.session.commit()
        

# how to do notifications?
# when listing is made, get all users who are subscribed
# for each subscribed user, get their preferred job categories and send notif to their email?