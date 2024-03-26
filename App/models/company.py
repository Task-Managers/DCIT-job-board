from App.database import db
from .user import User

class Company(User):
    # id = db.Column(db.Integer, primary_key = True)
    # id = db.Column(db.Integer)

    # company_name = db.Column(db.String, primary_key = True)
    company_name = db.Column(db.String, unique=True)

    # insert other company information here later
        # MAYBE SPECIFY BETWEEN COMPANY AND REPRESENTATIV ATTRIBUTES
     

    # set up relationship with Listing object (1-M)
    listings = db.relationship('Listing', backref='company', lazy=True)

    # maybe relationship with alumni? list of alumni as subscribers?
    # applicants?
    # applicants = db.relationship('Alumni', backref='company', lazy=True)

    def __init__(self, username, company_name, password, email):
        super().__init__(username, password, email)
        self.company_name = company_name
        
    def get_json(self):
        return{
            'id': self.id,
            'company_name': self.company_name,
            'email': self.email
        }
    
    def get_name(self):
        return self.company_name
    