from App.models import Listing, Company
from App.database import db

# add in getters, maybe put setters in company controllers

def get_listing(id):
    return User.query.get(id)

def get_all_listings():
    return Listing.query.all()

def get_all_listings_json():
    listings = get_all_listings()
    if not listings:
        return []
    listings = [listing.get_json() for listing in listings]
    return listings