from App.database import db
from .company import Company

categories = ['Software Engineering', 'Database', 'Programming', 'Web Design', 'Machine Learning', 'Big Data', 'Algorithms', 'N/A']

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(500))
    # insert other information later:
    # position type, options for remote, employment term, tt national, job areas, desired cand. type, level
    # use enums/ predetermined types maybe for some

    # categories = ['Software Engineering', 'Database', 'Programming', 'N/A']
    job_category = db.Column(db.String(120))
    # job_category = db.Column(ARRAY(db.String(120)))


    # set up relationship with Company (M-1)
    # company = db.Column(db.String(), db.ForeignKey('company.username'))
    # lister = db.relationship('Company')

    company_name = db.Column(db.String(), db.ForeignKey('company.company_name'), nullable=False)
    companies = db.relationship('Company', back_populates='listings', overlaps="company")

    # relationship with alumni?
    # each listing has applicants/alumni applied to it
    # subscribers = db.Column(db.String(), db.ForeignKey())

    def __init__(self, title, description, company_name, job_categories):
        self.title = title
        self.description = description
        self.company_name = company_name

        if job_categories is None:
            self.job_category = 'N/A'
        else:
            self.validate_and_set_categories(job_categories)

    def get_company(self):
        return self.company_name

    # methods to support adding, removing, validating the job categories
    def validate_and_set_categories(self, job_categories):
        valid_categories = [category for category in job_categories if category in categories]
        # for category in job_categories:
        #     if category not in categories:
        #         raise ValueError(f"Invalid job category: {category}")
        # self.job_category = '|'.join(job_categories)
        self.job_category = '|'.join(valid_categories)

    def get_categories(self):
        return self.job_category.split('|') if self.job_category else []

    def add_category(self, category):
        categories = self.get_categories()
        if category not in categories:
            categories.append(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' already exists.")

    def remove_category(self, category):
        categories = self.get_categories()
        if category in categories:
            categories.remove(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' does not exist.")

    def get_json(self):
        return{
            'id': self.id,
            'title':self.title,
            'description':self.description,
            'company_name':self.company_name,
            'job_category':self.get_categories(),
        }