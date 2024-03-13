import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users,
     add_admin, add_alumni, add_company, add_listing, 
     get_all_listings, get_all_listings_json, get_company_listings,
    subscribe_action, add_categories, )

# This commands file allow you to create convenient CLI commands for testing controllers
# test to see where this gets pushed to

# TODO:
# FIX ADDING IN CATEGORIES AND ALSO VALIDATING CATEGORES - FOR ALUMNI AND LISTING
# CHECK ALUMNI CONTROLLER FOR ADD_cATEGORIES FIRST, IT NOT SAVING TO DB?
# WHAT HAPPENS IF YOU ADD AN INVALID CATEOGORY USING THE CONTROLLER? - FOR ALUMNI AND LISTING

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    # add in the first admin
    add_admin('bob', 'bobpass', 'bob@mail')

    add_admin('bob2', 'bobpass', 'bob@mail2')

    # add in alumni
    add_alumni('rob', 'robpass', 'rob@mail', '12345')
    add_alumni('rob2', 'robpass', 'rob@mail2', '123452')

    print(add_categories('12345', ['Database']))
    # print('test')

    # subscribe rob
    subscribe_action('12345')

    # add in companies
    add_company('rep.name', 'company1', 'compass', 'company@mail')
    add_company('rep.name2', 'company2', 'compass', 'company@mail2')

    # add in listings
    add_listing('listing1', 'job description', 'company2')
    add_listing('listing2', 'job description', 'company2', ['Database', 'Programming', 'butt'])
    print(get_all_listings_json())
    # print(get_company_listings('company2'))
    
    # print all user
    print(get_all_users())
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(username, password):
#     create_user(username, password)
#     print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

# add in command groups and commands for:
# - admin
# - alumni 
# - business 
# - listing

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)