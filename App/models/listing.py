from App.database import db
from .company import Company

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(500))
    # insert other information later:
    # position type, options for remote, employment term, tt national, job areas, desired cand. type, level
    # use enums/ predetermined types maybe for some


    # set up relationship with Company (M-1)
    # company = db.Column(db.String(), db.ForeignKey('company.username'))
    # lister = db.relationship('Company')

    company_name = db.Column(db.String(), db.ForeignKey('company.company_name'), nullable=False)
    companies = db.relationship('Company', back_populates='listings', overlaps="company")
    
    # Define the relationship back to the Company model
    # company = db.relationship('Company', back_populates='listings', uselist=False, cascade="save-update, merge")

    # reviewerID = db.Column(
    #   db.String(10),
    #   db.ForeignKey('staff.ID'))  #each review has 1 creator

    #create reverse relationship from Staff back to Review to access reviews created by a specific staff member
#   reviewer = db.relationship('Staff',
#                              backref=db.backref('reviews_created',
#                                                 lazy='joined'),
#                              foreign_keys=[reviewerID])

    # relationship with alumni?
    # each listing has applicants/alumni applied to it

    def __init__(self, title, description, company_name):
        self.title = title
        self.description = description
        self.company_name = company_name

    def get_json(self):
        return{
            'id': self.id,
            'title':self.title,
            'description':self.description,
            'company_name':self.company_name
        }