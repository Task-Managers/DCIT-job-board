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