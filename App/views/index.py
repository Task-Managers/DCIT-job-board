from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, get_jwt_identity, current_user as jwt_current_user

from werkzeug.utils import secure_filename

from App.controllers import(
    add_admin,
    get_user_by_username,
    get_all_listings,
    get_all_listings_json,
)

from App.models import(
    Alumni
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

# @index_views.route('/', methods=['GET'])
# def index_page():
#     return render_template('homepage.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')
    add_admin('bob', 'bobpass', 'bob@mail')
    add_admin('bob2', 'bobpass', 'bob2@mail')

    return jsonify(message='db initialized!')

@index_views.route('/app', methods=['GET'])
# @index_views.route('/app/<int:category>', methods=['GET'])
@jwt_required()
def index_page():

    username = get_jwt_identity()
    user = get_user_by_username(username)

    # need to do:
    # - return a list of categories to render in
    # - return a list of listings - flesh out listing model 

    # job listings
    jobs = get_all_listings()
    # jobs = get_all_listings_json()
    print(jobs)
    
    # url = 'https://wger.de/api/v2/exercisecategory/?format=json'

    # response = requests.get(url)

    # if response.status_code == 200:
        
    #     categories = response.json()
    #     categories = categories['results']

    #     exercises_list = Exercise.query.filter_by(category=category)

    #     exerciseSets = ExerciseSet.query.filter_by(user_id = current_user.id)
    # return jsonify({'message': 'Welcome to the app route!', 'user': user}), 200
    if isinstance(user, Alumni):

        return render_template('alumni.html', jobs=jobs )

    return redirect('/login')

    # return render_template('homepage.html')
    # return render_template('index.html', categories = categories, exercises_list = exercises_list, exerciseSets = exerciseSets, user=user)

@index_views.route('/submit_application', methods=['POST'])
@jwt_required()
def submit_application_action():
    # get form data
    data = request.form

    # get current user
    username = get_jwt_identity()
    user = get_user_by_username(username)

    # get the files from the form
    resume_file = data['resume']
    cover_letter_file = data['cover_letter']

    # Save files to a folder
    resume_filename = secure_filename(resume_file.filename)
    cover_letter_filename = secure_filename(cover_letter_file.filename)
    resume_file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
    cover_letter_file_path = os.path.join(app.config['UPLOAD_FOLDER'], cover_letter_filename)
    resume_file.save(resume_file_path)
    cover_letter_file.save(cover_letter_file_path)

    # Create File objects
    resume = File(filename=resume_filename, filepath=resume_file_path, alumni_id=user.alumni_id)
    cover_letter = File(filename=cover_letter_filename, filepath=cover_letter_file_path, alumni_id=user.alumni_id)
    
    # Add files to database
    db.session.add(resume)
    db.session.add(cover_letter)
    db.session.commit()

    flash('Application submitted successfully!')
    return redirect('/app')
    

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})