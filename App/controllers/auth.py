from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies

from flask import jsonify

from App.models import User, Admin, Alumni, Company, Listing

def jwt_authenticate(username, password):

  admin = Admin.query.filter_by(username=username).first()
  if admin and admin.check_password(password):
    return create_access_token(identity=username)

  alumni = Alumni.query.filter_by(username=username).first()
  if alumni and alumni.check_password(password):
    return create_access_token(identity=username)

  company = Company.query.filter_by(username=username).first()
  if alumni and alumni.check_password(password):
    return create_access_token(identity=username)
  return None

def jwt_authenticate_admin(username, password):
  admin = Admin.query.filter_by(username=username).first()
  if admin and admin.check_password(password):
    return create_access_token(identity=username)

  return None

def login(username, password):
    # user = User.query.filter_by(username=username).first()
    # if user and user.check_password(password):
    #     return user

    user = None
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        # return admin
        user = admin

    alumni = Alumni.query.filter_by(username=username).first()
    if alumni and alumni.check_password(password):
        # return alumni
        user = alumni

    company = Company.query.filter_by(username=username).first()
    if company and company.check_password(password):
        # return company
        user = company
    if user is not None:
      token = create_access_token(identity=username)
      response = jsonify(access_token=token)
      set_access_cookies(response, token)
      return user
    return None
    # return None

# def login(username, password):
#     # user = User.query.filter_by(username=username).first()
#     User.query.filter_by(username=username).first()
#     if user and user.check_password(password):
#         return user
#     return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        # return User.query.get(user_id)
        admin = Admin.query.get(user_id)
        if admin:
          return admin
        
        alumni = Alumni.query.get(user_id)
        if alumni:
          return alumni

        company = Company.query.get(user_id)
        if company:
          return company
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        # user = User.query.filter_by(username=identity).one_or_none()
        # if user:
        #     return user.id
        # return None
        admin = Admin.query.filter_by(username=identity).one_or_none()
        if admin:
          return admin.id

        alumni = Alumni.query.filter_by(username=identity).one_or_none()
        if alumni:
          return alumni.id

        company = Company.query.filter_by(username=identity).one_or_none()
        if company:
          return company.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        # return User.query.get(identity)

        admin = Admin.query.filter_by(username=identity).one_or_none()
        if admin:
            return admin

        alumni = Alumni.query.filter_by(username=identity).one_or_none()
        if alumni:
          return alumni

        company = Company.query.filter_by(username=identity).one_or_none()
        if company:
          return company

    return jwt