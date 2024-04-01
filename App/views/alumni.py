# import random
# import string
from flask import Blueprint, request, jsonify, flash, redirect, render_template
# from App.controllers import Student, Staff
# from App.controllers.user import get_staff, get_student
from App.database import db
from flask_jwt_extended import current_user 
from flask_jwt_extended import jwt_required

from App.controllers import (
    login
)

from App.controllers.alumni import *

alumni_views = Blueprint('alumni_views', __name__, template_folder='../templates')

# @alumni_views.route('/', methods=['GET'])
# @alumni_views.route('/login', methods=['GET'])
# # @jwt_required
# def login_page():
#   if current_user.is_authenticated:
#     return redirect('/app')
#   return render_template('homepage.html')

# @alumni_views.route('/login', methods=['POST'])
# def login_action():

#     data = request.form
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
    
#     if user and user.check_password(data['password']):  # check credentials
#         flash('Logged in successfully.')  # send message to next page
#         # login_user(user)  # login the user
#         login(user.username, user.password)
#         return redirect('/app')  # redirect to main page if login successful
#         # return render_template('homepage.html')
#     else:
#         flash('Invalid username or password')  # send message to next page
#     return redirect('/')