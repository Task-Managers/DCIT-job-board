from App.database import db
from .company import Company

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(500))
    # insert other information later:
    # position type, options for remote, employment term, tt national, job areas, desired cand. type, level
    # use enums/ predetermined types maybe for some

    categories = ['Software Engineering', 'Database', 'Programming', 'N/A']
    job_category = db.Column(db.String(120))


    # set up relationship with Company (M-1)
    # company = db.Column(db.String(), db.ForeignKey('company.username'))
    # lister = db.relationship('Company')

    company_name = db.Column(db.String(), db.ForeignKey('company.company_name'), nullable=False)
    companies = db.relationship('Company', back_populates='listings', overlaps="company")

    # relationship with alumni?
    # each listing has applicants/alumni applied to it
    # subscribers = db.Column(db.String(), db.ForeignKey())

    def __init__(self, title, description, company_name, job_category):
        self.title = title
        self.description = description
        self.company_name = company_name

        if job_category is None:
            self.job_category = 'N/A'

        if job_category in self.categories:
            self.job_category = job_category
        else:
            self.job_category = 'N/A'

    def get_json(self):
        return{
            'id': self.id,
            'title':self.title,
            'description':self.description,
            'company_name':self.company_name,
            'job_category':self.job_category,
        }