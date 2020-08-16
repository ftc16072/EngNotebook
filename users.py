import hashlib
import sqlite3
import re
import os
import json
from passlib.apps import custom_app_context as pwd_context


def make_safe_name(input):
    return re.sub(r'\W+', '', input)


class User(object):
    def __init__(self, username, team):
        self.username = username
        self.team = team
        self.databaseName = 'data/' + make_safe_name(self.team) + '.sqlite3'

    def dbConnect(self):
        return sqlite3.connect(self.databaseName,
                               detect_types=sqlite3.PARSE_DECLTYPES)


class Users(object):
    def __init__(self):
        self.users = {}
        if not os.path.exists('data'):
            os.makedirs('data')
        self.path = os.path.join('data', 'users.json')
        try:
            with open(self.path, 'r') as user_file:
                self.users = json.loads(user_file.read())
        except IOError:
            pass

    def save(self):
        with open(self.path, 'w') as user_file:
            json.dump(self.users, user_file)

# if username already exists, this overwrites it.   So be careful upon calling it!

    def add(self, username, team, password):
        username = username.lower()
        self.users[username] = {}
        self.users[username]['password'] = pwd_context.hash(password)
        self.users[username]['team'] = team.lower()
        self.save()

    def change_password(self, username, newpass):
        self.users[username]['password'] = pwd_context.hash(newpass)
        self.save()

    def getUser(self, username, password):
        if username and username in self.users and pwd_context.verify(
                password, self.users[username]['password']):
            return User(username, self.users[username]['team'])
        else:
            return None


# unit test
if __name__ == "__main__":
    users = Users()
    users.add('alan@randomsmiths.com', 'ftc16072', 'password')

    # Check good login
    user = users.getUser('alan@randomsmiths.com', 'password')
    if not user:
        print('Failure verifying good one')
    print(f'Success: {user.databaseName}')

    # Check bad password
    user = users.getUser('alan@randomsmiths.com', 'badpass')
    if user:
        print("Shouldn't have validated")
    # Check no account
    user = users.getUser('noaccount', 'password')
    if user:
        print("Shouldn't have validated")
