from App.models import User, Alumni, Admin, Company, Listing
from App.database import db


def add_alumni(username, name, password, email, alumni_id, contact):

        # Check if there are no other users with the same username or email values in any other subclass
        if (
            # Alumni.query.filter_by(username=username).first() is not None or
            Admin.query.filter_by(username=username).first() is not None or
            Company.query.filter_by(username=username).first() is not None or

            Company.query.filter_by(email=email).first() is not None or
            Admin.query.filter_by(email=email).first() is not None
            # Alumni.query.filter_by(email=email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newAlumni= Alumni(username, name, password, email, alumni_id, contact)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newAlumni)
            db.session.commit()  # Commit to save the new  to the database
            return newAlumni
        except:
            db.session.rollback()
            return None

def get_all_alumni():
    return db.session.query(Alumni).all()

def get_all_alumni_json():
    alumnis = get_all_alumni()
    if not alumnis:
        return []
    alumnis = [alumni.get_json() for alumni in alumnis]
    return alumnis

def get_alumni(alumni_id):
    return Alumni.query.filter_by(alumni_id=alumni_id).first()

def is_alumni_subscribed(alumni_id):
    alumni = get_alumni(alumni_id)

    if(alumni.subscribed == True):
        return True
    else:
        return False

def get_all_subscribed_alumni():
    all_alumni = Alumni.query.filter_by(subscribed=True).all()
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
    db.session.commit()
    return alumni
        
# adding and removing job categories 
def add_categories(alumni_id, job_categories):
    alumni = get_alumni(alumni_id)
    try:
        for category in job_categories:
            # print(category)
            alumni.add_category(category)
            # print(alumni.get_categories())
            db.session.commit()
        return alumni
    except:
        db.session.rollback()
        return None   

# apply to an application
def apply_listing(alumni_id, listing_title):
    from App.controllers import get_listing_title

    alumni = get_alumni(alumni_id)

    # error check to see if alumni exists
    if alumni is None:
        return None

    # get the listing and then company that made the listing
    listing = get_listing_title(listing_title)

    if listing is None:
        return None

    # add the alumni to the listing applicant
    listing.applicant.append(alumni)
    alumni.listing.append(listing)

    #commit changes to the database
    db.session.commit()

    # add the alumni as an applicant to the company model object?

    return alumni