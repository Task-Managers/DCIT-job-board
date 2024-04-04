from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies, current_user as jwt_current_user
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
    login,
    login_user
)

from App.controllers.alumni import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/', methods=['GET'])
@user_views.route('/login', methods=['GET'])
# @jwt_required()
def login_page():
#   if current_user.is_authenticated:
#     return redirect('/app')
  return render_template('homepage.html')

@user_views.route('/login', methods=['POST'])
def login_action():
  data = request.form
  token = login_user(data['username'], data['password'])

  print(token)
  print('testttttttt')

  response = None
  if token:
    flash('Logged in successfully.')  # send message to next page
    response = redirect(url_for('auth_views.identify_page'))
    # response = redirect('/')
    set_access_cookies(response, token)
  else:
    flash('Invalid username or password')  # send message to next page
    response = redirect('/')
  return response

# @user_views.route('/login', methods=['POST'])
# def login_action():

#     data = request.form
#     response = login(data['username'], data['password'])

#     if response:
#         flash('Logged in successfully!')
#         print(response)
#         return redirect('/identify')
#         # return(current_user)
#     else:
#         flash('Invalid username or password')
#         return redirect('/')
    
#     # if user and user.check_password(data['password']):  # check credentials
#     #     flash('Logged in successfully.')  # send message to next page

#     #     # token = create_access_token(identity=username)
#     #     # response = jsonify(access_token=token)
#     #     # set_access_cookies(response, token)

#     #     # login(user.username, user.password)
#     #     # return redirect('/app')  # redirect to main page if login successful
#     #     # return render_template('homepage.html')

#     #     return(user.get_json())
#     #     # return(current_user)
#     # else:
#     #     flash('Invalid username or password')  # send message to next page
#     # return redirect('/')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    # users = get_all_users_json()
    users = get_all_users_json()
    return jsonify(users)
    # return users[0]['username']

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