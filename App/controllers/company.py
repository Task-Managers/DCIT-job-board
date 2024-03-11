from App.models import User, Company, Listing
from App.database import db



def add_company(username, company_name, password, email):
        newCompany= Company(username,company_name, password, email)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newCompany)
            db.session.commit()  # Commit to save the new  to the database
            return newCompany
        except:
            db.session.rollback()
            return None

def add_listing(title, description, company_name, job_category=None):

    # manually validate that the company actually exists
    company = get_company_by_name(company_name)
    if not company:
        return None

    newListing = Listing(title, description, company_name, job_category)
    try:
        db.session.add(newListing)
        db.session.commit()
        return newListing
    except:
        db.session.rollback()
        return None

def get_company_by_name(company_name):
    return Company.query.filter_by(company_name=company_name).first()
