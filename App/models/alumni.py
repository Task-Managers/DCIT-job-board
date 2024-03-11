from App.database import db
from .user import User

class Alumni(User):
    id = db.Column(db.Integer, primary_key = True)
    alumni_id = db.Column(db.Integer, nullable = False, unique = True)
    # insert other personal info later


    # relationship to companies 
    # company_name = db.Column(db.String(), db.ForeignKey('company.company_name'), nullable=False)
    # companies = db.relationship('Company', back_populates='subscribers', overlaps="company")

    # relationship to listings to receive notifications?
    subscribed = db.Column(db.Boolean, default=False)


    def __init__(self, username, password, email, alumni_id):
        super().__init__(username, password, email)
        self.alumni_id = alumni_id

    def get_alumni_id(self):
        return self.alumni_id

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'alumni_id': self.alumni_id,
            'subscribed': self.subscribed,
        }