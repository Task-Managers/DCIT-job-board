from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, set_access_cookies, current_user as jwt_current_user
from flask_login import current_user, login_required

from flask_wtf.csrf import generate_csrf

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    # jwt_authenticate_admin,
    get_all_users,

    add_company,

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
def login_page():
  return render_template('homepage.html')

@user_views.route('/signup', methods=['GET'])
def signup_page():
  return render_template('homepage.html')

@user_views.route('/login', methods=['POST'])
def login_action():
  data = request.form
  token = login_user(data['username'], data['password'])
  
  print(token)
  response = None
  
  if token:
    flash('Logged in successfully.')  # send message to next page
    response = redirect(url_for('index_views.index_page'))
    set_access_cookies(response, token)
  else:
    flash('Invalid username or password')  # send message to next page
    response = redirect('/')

  csrf_token = generate_csrf()
  response.headers["X-CSRF-TOKEN"] = csrf_token

  print('response headers: ', response.headers)
  return response

@user_views.route('/alumni-signup', methods=['POST'])
def alumni_signup_action():
  data = request.form
  
  response = None

  try:
    newAlumni = add_alumni(data['username'], data['password'], data['email'],
                          data['alumni_id'], data['contact'], data['firstname'], data['lastname'])

    token = login_user(data['username'], data['password'])

    print(token)

    response = redirect(url_for('index_views.index_page'))
    set_access_cookies(response, token)
    flash('Account created!')

    csrf_token = generate_csrf()
    response.headers["X-CSRF-TOKEN"] = csrf_token

  except Exception:  # attempted to insert a duplicate user
    db.session.rollback()
    flash("username or email already exists")  # error message
    response = redirect(url_for('login_page'))

  return response

@user_views.route('/company-signup', methods=['POST'])
def company_signup_action():
  data = request.form
  
  response = None

  try:
    # newAlumni = add_alumni(data['username'], data['password'], data['email'],
    #                       data['alumni_id'], data['contact'], data['firstname'], data['lastname'])
    newCompany = add_company(data['username'], data['company_name'], data['password'], data['email'],
                              data['company_address'], data['contact'], data['company_website'])
    # username, company_name, password, email, company_address, contact, company_website
    token = login_user(data['username'], data['password'])

    print(token)

    response = redirect(url_for('index_views.index_page'))
    set_access_cookies(response, token)
    flash('Account created!')

    csrf_token = generate_csrf()
    response.headers["X-CSRF-TOKEN"] = csrf_token

  except Exception:  # attempted to insert a duplicate user
    db.session.rollback()
    flash("username or email already exists")  # error message
    response = redirect(url_for('login_page'))

  return response

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