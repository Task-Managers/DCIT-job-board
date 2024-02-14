from App.database import db
from .user import User

class Company(User):
    id = db.Column(db.Integer, primary_key = True)
    # insert other company information here later
        # MAYBE SPECIFY BETWEEN COMPANY AND REPRESENTATIV ATTRIBUTES
     

    # set up relationship with Listing object (1-M)

    # maybe relationship with alumni? list of alumni as subscribers?

    def __init__(self, username, password, email):
        super().__init__(username, password, email)

    