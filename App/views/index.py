from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
# from App.controllers import create_user

# from flask_jwt_extended import current_user 
# from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('homepage.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/app', methods=['GET'])
# @index_views.route('/app/<int:category>', methods=['GET'])
#need to set up login things
@jwt_required
def index_page():
    # user = current_user
    user = get_jwt_identiy()
    # url = 'https://wger.de/api/v2/exercisecategory/?format=json'

    # response = requests.get(url)

    # if response.status_code == 200:
        
    #     categories = response.json()
    #     categories = categories['results']

    #     exercises_list = Exercise.query.filter_by(category=category)

    #     exerciseSets = ExerciseSet.query.filter_by(user_id = current_user.id)
    return jsonify({'message': 'Welcome to the app route!', 'user': user}), 200
    if isinstance(user, Alumni):

        return render_template('alumni.html')

    # return render_template('homepage.html')
    # return render_template('index.html', categories = categories, exercises_list = exercises_list, exerciseSets = exerciseSets, user=user)


@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})