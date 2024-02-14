from App.models import User, Company, Listing
from App.database import db

def add_company(username, password, email):
        newCompany= Company(username, password, email)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newCompany)
            db.session.commit()  # Commit to save the new  to the database
            return newCompany
        except:
            db.session.rollback()
            return None

def add_listing(title, description):
    newListing = Listing(title, description)
    try:
        db.session.add(newListing)
        db.session.commit()
        return newListing
    except:
        db.session.rollback()
        return None