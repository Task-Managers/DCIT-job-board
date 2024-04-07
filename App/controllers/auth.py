from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies

from flask import jsonify

from App.models import User, Admin, Alumni, Company, Listing

from App.controllers import get_user_by_username

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
    user = get_user_by_username(username)
    if user and user.check_password(password):
    # if user is not None:
      token = create_access_token(identity=username)
      response = jsonify(access_token=token)
      set_access_cookies(response, token)
      return response
    # return jsonify(message="Invalid username or password"), 401
    return None

def login_user(username, password):
  # user = User.query.filter_by(username=username).first()
  user = get_user_by_username(username)
  
  if user and user.check_password(password):
    token = create_access_token(identity=username)
    print('token created')
    return (token)
  return None

def logout(username, password):

  return None

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
    # def load_user(user_id):
    def load_user(username):
        # return User.query.get(user_id)
        # admin = Admin.query.get(username)
        admin = Admin.query.filter_by(username=username).first()
        if admin:
          return admin
        
        # alumni = Alumni.query.get(username)
        alumni = Alumni.query.filter_by(username=username).first()
        if alumni:
          return alumni

        # company = Company.query.get(username)
        company = Company.query.filter_by(username=username).first()
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
          return admin.username
          # return admin.id

        alumni = Alumni.query.filter_by(username=identity).one_or_none()
        if alumni:
          return alumni.username
          # return alumni.id

        company = Company.query.filter_by(username=identity).one_or_none()
        if company:
          return company.username
          # company.id

        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        # return User.query.get(identity)

        admin = Admin.query.filter_by(username=identity).one_or_none()
        # admin = Admin.query.get(identity)
        if admin:
            return admin

        alumni = Alumni.query.filter_by(username=identity).one_or_none()
        # alumni = Alumni.query.get(identity)
        if alumni:
          return alumni

        company = Company.query.filter_by(username=identity).one_or_none()
        # company = Company.query.get(identity)
        if company:
          return company
    return jwt

# def login_required(required_class):
#   def wrapper(f):
#       @wraps(f)
#       @jwt_required()  # Ensure JWT authentication
#       def decorated_function(*args, **kwargs):
#         user = required_class.query.filter_by(username=get_jwt_identity()).first()  
#         print(user.__class__, required_class, user.__class__ == required_class)
#         if user.__class__ != required_class:  # Check class equality
#             return jsonify(message='Invalid user role'), 403
#         return f(*args, **kwargs)
#       return decorated_function
#   return wrapper

def alumni_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Alumni):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper


def Company_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Company):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper