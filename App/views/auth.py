from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    login,
    login_user,
    get_user_by_username,
    get_all_users,
    admin_required, 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
# @login_required
@jwt_required()
def identify_page():
    # return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})
    username = get_jwt_identity()
    # username = jwt_current_user.username
    # user = User.query.filter_by(username=username).first()
    # print('username')
    user = get_user_by_username(username)
    if user:
        return jsonify(user.get_json())
    return jsonify(message='Invalid user'), 403


# @auth_views.route('/login', methods=['POST'])
# def login_action():
#     data = request.form
#     user = login(data['username'], data['password'])
#     if user:
#         login_user(user)
#         return 'user logged in!'
#     return 'bad username or password given', 401

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    data = request.form
    user = login(data['username'], data['password'])
    return 'logged out!'

'''
API Routes
'''

@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return None

# @auth_views.route('/api/users', methods=['POST'])
# def create_user_endpoint():
#     data = request.json
#     create_user(data['username'], data['password'])
#     return jsonify({'message': f"user {data['username']} created"})

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
#   token = jwt_authenticate(data['username'], data['password'])
    response = login(data['username'], data['password'])
    if not response:
        return jsonify(message='bad username or password given'), 401
    # return jsonify(access_token=token)
    return response

# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
#     data = request.json
#     token = login_user(data['username'], data['password'])
#     # token = jsonify(access_token=token)
#     # print(token)
#     # print('testttttttt')

#     response = None
    
#     if token:
#         flash('Logged in successfully.')  # send message to next page
#         response = redirect(url_for('auth_views.identify_page'), token)
#         # response = redirect('/identify')
#         set_access_cookies(response, token)
#     else:
#         flash('Invalid username or password')  # send message to next page
#         response = redirect('/')
#     print(response)
#     return response
#     # return jsonify(access_token=token)

@auth_views.route('/api/logout', methods=['GET'])
def logout():
  response = jsonify(message='Logged out')
  unset_jwt_cookies(response)
  return response

# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# # @login_required
# def identify_user_action():
#     user = get_jwt_identity()
#     return jsonify(user.get_json())