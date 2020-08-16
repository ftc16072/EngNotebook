import os
import sqlite3
import json
import cherrypy

from mako.lookup import TemplateLookup

import users

smugmugConfig = {}


class Cookie(object):
    """Abstracts cookies so they can be in sessions"""
    def __init__(self, name):
        self.name = name

    def get(self, default=''):
        """Get the value of the cookie or set if doesn't exist"""
        if self.name in cherrypy.session:
            return cherrypy.session[self.name]
        else:
            self.set(default)
            return default

    def set(self, value):
        """Set the value of the cookie"""
        cherrypy.session[self.name] = value


class FtcNotebook(object):
    def __init__(self):
        self.lookup = TemplateLookup(directories=['HtmlTemplates'],
                                     default_filters=['h'])

    def template(self, template_name, **kwargs):
        return self.lookup.get_template(template_name).render(**kwargs)

    def getUser(self):
        username = Cookie('username').get()
        team = Cookie('team').get()
        if not username or not team:
            return None
        return users.User(username, team)

    def show_loginpage(self, error=''):
        """Clear session and show login page"""
        cherrypy.session.regenerate()
        return self.template("login.mako", error=error)

    def show_mainpage(self, user, error=''):
        return f'{user.username} on {user.team}'

    @cherrypy.expose
    def index(self):
        """Shows main page or forces login if not logged in"""
        user = self.getUser()
        if not user:
            return self.show_loginpage('')
        return self.show_mainpage(user)

    @cherrypy.expose
    def login(self, username, password):
        user = users.Users().getUser(username, password)
        if user:
            Cookie('username').set(user.username)
            Cookie('team').set(user.team)
            return self.show_mainpage(user)
        return self.show_loginpage('Not a valid username/password pair')


if __name__ == "__main__":
    smugmugConfig = json.load(open('secrets.json', 'r'))
    cherrypy.quickstart(FtcNotebook(), config='development.conf')
