import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    jwt_authenticate_admin,
    get_user,
    get_user_by_username,
    update_user,
    add_admin
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", 'bob@mail')
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password, 'bob@mail')
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password, 'bob@mail')
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


# def test_authenticate():
#     user = add_admin("bob", "bobpass", 'bob@mail')
#     # assert login("bob", "bobpass") != None
#     token = jwt_authenticate_admin('bob', "bobpass")
#     assert token is not None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        add_admin("bob", "bobpass", 'bob@mail')
        user = add_admin("rick", "bobpass", 'rick@mail')
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob", 'email':'bob@mail'}, {"id":2, "username":"rick", 'email':'rick@mail'}], users_json)

    # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username = "ronnie"
        

