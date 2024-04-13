from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, get_jwt_identity, current_user as jwt_current_user

# from flask_wtf.csrf import CSRFProtect
# csrf = CSRFProtect()

from werkzeug.utils import secure_filename

from App.controllers import(
    add_admin,
    get_user_by_username,
    get_all_listings,
    get_company_listings,
    add_listing,
    apply_listing,
)

from App.models import(
    Alumni,
    Company
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
    
    # return jsonify({'message': 'Welcome to the app route!', 'user': user}), 200
    if isinstance(user, Alumni):

        return render_template('alumni.html', jobs=jobs )

    if isinstance(user, Company):
        jobs = get_company_listings(username)
        return render_template('company-view.html', jobs=jobs)

    return redirect('/login')

    # return render_template('homepage.html')
    # return render_template('index.html', categories = categories, exercises_list = exercises_list, exerciseSets = exerciseSets, user=user)
@index_views.route('/add_listing', methods=['GET'])
@jwt_required()
def add_listing_page():
    # username = get_jwt_identity()
    # user = get_user_by_username(username)

    return render_template('companyform.html')

@index_views.route('/add_listing', methods=['POST'])
@jwt_required()
def add_listing_action():
    # username = get_jwt_identity()
    # user = get_user_by_username(username)
    data = request.form

    

    return render_template('companyform.html')

@index_views.route('/submit_application', methods=['POST'])
@jwt_required()
def submit_application_action():
    # get form data

    expected_csrf_token = generate_csrf()
    # Get CSRF token from form data
    submitted_csrf_token = request.form.get('csrf_token')

    if submitted_csrf_token == expected_csrf_token:
        return redirect('/app')
    else:
        return redirect('/login')

    data = request.form

    # print(session.get('csrf-token'))

    # get current user
    username = get_jwt_identity()
    user = get_user_by_username(username)

    response = None

    try:
        alumni = apply_listing(user.alumni_id, data['job_id'])
        response = redirect(url_for('index_views.index_page'))
        flash('Application submitted')

        csrf_token = generate_csrf()
        response.headers["X-CSRF-TOKEN"] = csrf_token

    except Exception:
        db.session.rollback()
        flash('Error submitting application')
        response = redirect(url_for('index_page'))

    return response

    # get the files from the form
    print('testttt')
    print(data)

    # deal with file handling for reumse and cover_letter files
    # resume_file = data['resume']
    # cover_letter_file = data['cover_letter']

    # # Save files to a folder
    # resume_filename = secure_filename(resume_file.filename)
    # cover_letter_filename = secure_filename(cover_letter_file.filename)
    # resume_file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
    # cover_letter_file_path = os.path.join(app.config['UPLOAD_FOLDER'], cover_letter_filename)
    # resume_file.save(resume_file_path)
    # cover_letter_file.save(cover_letter_file_path)

    # # Create File objects
    # resume = File(filename=resume_filename, filepath=resume_file_path, alumni_id=user.alumni_id)
    # cover_letter = File(filename=cover_letter_filename, filepath=cover_letter_file_path, alumni_id=user.alumni_id)
    
    # # Add files to database
    # db.session.add(resume)
    # db.session.add(cover_letter)
    # db.session.commit()

    # flash('Application submitted successfully!')
    return redirect('/app')
    

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})