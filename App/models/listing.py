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

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def get_json(self):
        return{
            'id': self.id,
            'title':self.title,
            'description':self.description
        }