from App.database import db
from .user import User

class Alumni(User):
    id = db.Column(db.Integer, primary_key = True)
    alumni_id = db.Column(db.Integer, nullable = False, unique = True)
    # insert other personal info later

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
            'alumni_id': self.alumni_id
        }