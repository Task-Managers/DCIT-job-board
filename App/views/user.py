from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    # jwt_authenticate_admin,
    get_all_users,

    get_user_by_username,

    get_all_users_json,
    jwt_required,
    login
)

from App.controllers.alumni import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/login', methods=['POST'])
def login_action():

    data = request.form
#     user = None
# #   user = User.query.filter_by(username=data['username']).first()
#     alumni = Alumni.query.filter_by(username=data['username']).first()
#     if alumni:
#         user = alumni
#     admin = Admin.query.filter_by(username=data['username']).first()
#     if admin:
#         user = admin
#     company = Company.query.filter_by(username=data['username']).first()
#     if company:
#         user = company
    user = get_user_by_username(data['username'])
    
    if user and user.check_password(data['password']):  # check credentials
        flash('Logged in successfully.')  # send message to next page
        # login_user(user)  # login the user
        login(user.username, user.password)
        # return redirect('/app')  # redirect to main page if login successful
        # return render_template('homepage.html')
        return(user.get_json())
    else:
        flash('Invalid username or password')  # send message to next page
    return redirect('/')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')