import datetime
import os
import sqlite3
import json
import argparse
import cherrypy

from mako.lookup import TemplateLookup

import users
from tasks import Tasks, Task, TaskStages
import smugmug

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
        with user.team.dbConnect() as connection:
            dateList = user.team.entries.getDateList(connection)
            taskList = user.team.entries.tasks.getAllTaskList(connection)

        return self.template('home.mako',
                             dateList=dateList,
                             taskList=taskList,
                             destination="Screen")

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
            Cookie('team').set(user.team.teamName)
            return self.show_mainpage(user)
        return self.show_loginpage('Not a valid username/password pair')

    @cherrypy.expose
    def logout(self):
        return self.show_loginpage()

    @cherrypy.expose
    def listEntries(self):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')

        with user.team.dbConnect() as connection:
            dateList = user.team.entries.getDateList(connection)

        return self.template('entries.mako', dateList=dateList)

    @cherrypy.expose
    def newEntry(self):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        with user.team.dbConnect() as connection:
            memberList = user.team.entries.members.getMembers(connection)
            taskList = user.team.entries.tasks.getWorkingTaskList(connection)
        return self.template('engNotebookForm.mako',
                             dateString=date,
                             members=memberList,
                             tasks=taskList)

    @cherrypy.expose
    def addEntry(self, dateString, memberId, taskId, hours, accomplished, why,
                 learning, next_steps, notes, diagram, photo):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')

        with user.team.dbConnect() as connection:
            if photo.filename:
                imgKey = smugmug.upload_data(connection, photo.filename,
                                             photo.file.read(), smugmugConfig,
                                             dateString)
            else:
                imgKey = ""
            user.team.entries.addEntry(connection, dateString, taskId,
                                       memberId, hours, accomplished, why,
                                       learning, next_steps, notes, diagram,
                                       imgKey, smugmugConfig)

        return self.newEntry()

    @cherrypy.expose
    def tasksForm(self):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')
        taskStages = TaskStages
        with user.team.dbConnect() as connection:
            taskList = user.team.entries.tasks.getAllTaskList(connection)
        return self.template('tasksForm.mako',
                             taskList=taskList,
                             TaskStages=taskStages)

    @cherrypy.expose
    def updateTasks(self, **kwargs):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')

        taskdict = dict(**kwargs)
        with user.team.dbConnect() as connection:
            for (k, v) in taskdict.items():
                user.team.entries.tasks.changeState(connection,
                                                    taskId=k,
                                                    newState=v)
        return self.tasksForm()

    @cherrypy.expose
    def addTasks(self, task, stage):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')

        with user.team.dbConnect() as connection:
            user.team.entries.tasks.addTask(dbConnection=connection,
                                            name=task,
                                            stage=stage)
        return self.tasksForm()

    @cherrypy.expose
    def viewEntry(self, dateString, destination):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')

        previousEntry = ''
        nextEntry = ''

        with user.team.dbConnect() as connection:
            tasksDictionary = user.team.entries.getDateTasksDictionary(
                dateString, connection, smugmugConfig)
            (previousEntry, nextEntry) = user.team.entries.getPrevNext(
                connection, dateString)
        return self.template('viewEntry.mako',
                             previousEntry=previousEntry,
                             nextEntry=nextEntry,
                             tasksDictionary=tasksDictionary,
                             pageTitle=dateString,
                             destination=destination)

    @cherrypy.expose
    def viewTask(self, taskId, destination="Screen"):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')

        with user.team.dbConnect() as connection:
            (dateDictionary, taskName) = user.team.entries.getDateDictionary(
                taskId, connection, smugmugConfig)
        return self.template('viewTask.mako',
                             dateDictionary=dateDictionary,
                             pageTitle=taskName,
                             destination=destination)

    @cherrypy.expose
    def viewTaskByName(self, taskName, destination="Screen"):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')

        with user.team.dbConnect() as connection:
            taskId = user.team.entries.tasks.getTaskId(connection, taskName)
        return self.viewTask(taskId, destination)

    @cherrypy.expose
    def hours(self):
        user = self.getUser()
        if not user:
            return self.show_loginpage('')
        with user.team.dbConnect() as connection:
            entries = user.team.entries.getEntriesWithHours(connection)
        return self.template('viewHours.mako',
                             entries=entries,
                             pageTitle="Hours")

    @cherrypy.expose
    def gotoSmugmug(self, imgkey):
        new_url = smugmug.getLargestImage(imgkey, smugmugConfig)
        raise cherrypy.HTTPRedirect(new_url, status=301)


if __name__ == "__main__":
    smugmugConfig = json.load(open('secrets.json', 'r'))
    parser = argparse.ArgumentParser(
        description="FtcNotebook - for creating ftc notebooks")
    parser.add_argument('conf')
    args = parser.parse_args()

    cherrypy.config.update(args.conf)
    cherrypy.quickstart(FtcNotebook(), '', args.conf)
