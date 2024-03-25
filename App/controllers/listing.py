from App.models import Listing, Company
from App.database import db

# add in getters, maybe put setters in company controllers

def get_listing(id):
    return Listing.query.filter_by(id=id).first()

def get_listing_title(listing_title):
    return Listing.query.filter_by(title=listing_title).first()

def get_all_listings():
    return Listing.query.all()

def get_all_applicants(id):
    listing = get_listing(id)
    return listing.get_applicants()

def get_all_listings_json():
    listings = get_all_listings()
    if not listings:
        return []
    listings = [listing.get_json() for listing in listings]
    return listings

# get all listings by company name