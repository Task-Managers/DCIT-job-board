from App.database import db
# from .alumni import Alumni

from flask import request, session
from werkzeug.utils import secure_filename

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.alumni_id'), nullable=False)

    alumni = db.relationship('Alumni', back_populates='files')


    def __init__(self, filename, filepath, alumni_id):
        self.filename = filename
        self.filepath = filepath
        self.alumni_id = alumni_id

    def get_json(self):
        return{
            'id':self.id,
            'filename':self.filename,
            'filepath':self.filepath,
            'alumni_id':self.alumni_id,
        }