import os
import io
import zipfile
import yaml
import sqlite3
import json
import cherrypy
from cherrypy.lib import static
from mako.lookup import TemplateLookup
import datetime
import glob
import users
from entries import Entries
from tasks import Tasks, Task, TaskStages
from members import Members, Member
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
        self.lookup = TemplateLookup(directories = ['HtmlTemplates'], default_filters=['h'])
        self.latexLookup = TemplateLookup(directories = ['laTeXTempletes'], default_filters=['h'])
        self.tasks = Tasks()
        self.members = Members()
        self.entries = Entries()
        with self.dbConnect() as connection:
            if not os.path.exists(DB_STRING):
                self.entries.createTable(connection)
            else:
                data = connection.execute("PRAGMA schema_version").fetchone()
                if data[0] != self.entries.SCHEMA_VERSION:
                    self.entries.migrate(connection, data[0])

    def dbConnect(self):
        return sqlite3.connect(DB_STRING, detect_types=sqlite3.PARSE_DECLTYPES)

    def template(self, template_name, **kwargs):
        return self.lookup.get_template(template_name).render(**kwargs)
    
    def LaTeXtemplate(self, template_name, **kwargs):
        return self.latexLookup.get_template(template_name).render(**kwargs)

    def LaTeXtemplate(self, template_name, **kwargs):
        return self.latexLookup.get_template(template_name).render(**kwargs)

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
                 learning, next_steps, notes, diagramDot, photo):
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
                                       learning, next_steps, notes, diagramDot,
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
        
        with self.dbConnect() as connection:
            tasksDictionary = self.entries.getDateTasksDictionary(dateString, connection, smugmugConfig)
            (previousEntry, nextEntry) = self.entries.getPrevNext(connection, dateString)
        if destination == "download":
            path = "data/entryTex.tex"
            try:
                os.remove(path)
            except IOError:
                pass  #delete File, if it doesn't exist we don't care
            with open(path, "a") as file:
                monthName = datetime.date(2020, int(dateString[5:-3]),
                                          1).strftime('%B')
                wholedate = monthName + " " + dateString[-2:]
                file.write(
                    self.LaTeXtemplate('viewEntry.mako',
                                       date=wholedate,
                                       taskDict=tasksDictionary))
            fullpath = os.path.join(os.path.dirname(__file__), path)
            print(os.path.dirname(__file__))
            print(fullpath)
            return static.serve_file(os.path.abspath(fullpath),
                                     'application/x-download', 'entryTex',
                                     os.path.basename(path))

        else:
            return self.template('viewEntry.mako',
                                 previousEntry=previousEntry,
                                 nextEntry=nextEntry,
                                 tasksDictionary=tasksDictionary,
                                 pageTitle=dateString,
                                 destination=destination)


        with user.team.dbConnect() as connection:
            tasksDictionary = user.team.entries.getDateTasksDictionary(
                dateString, connection, smugmugConfig)
            (previousEntry, nextEntry) = user.team.entries.getPrevNext(
                connection, dateString)

        if destination == "download":
            path = "data/" + dateString + ".tex"
            try:
                os.remove(path)
            except IOError:
                pass  #delete File, if it doesn't exist we don't care
            with open(path, "a") as file:
                monthName = datetime.date(2020, int(dateString[5:-3]),
                                          1).strftime('%B')
                wholedate = monthName + " " + dateString[-2:]
                file.write(
                    self.LaTeXtemplate('viewEntry.mako',
                                       date=wholedate,
                                       taskDict=tasksDictionary))
            fullpath = os.path.join(os.path.dirname(__file__), path)
            print(os.path.dirname(__file__))
            print(fullpath)
            return static.serve_file(os.path.abspath(fullpath),
                                     'application/x-download', 'entryTex',
                                     os.path.basename(path))

        else:
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
        smugConfig = json.load(open('secrets.json', 'r'))
        new_url = smugmug.getLargestImage(imgkey, smugConfig)
        raise cherrypy.HTTPRedirect(new_url, status=301)


    @cherrypy.expose
    def downloadAll(self):
        latexFiles = io.BytesIO()
        ''' with self.dbConnect() as connection:
                dateList = self.entries.getDateList(connection)
                
                    file.write(self.LaTeXtemplate('viewEntry.mako', date=wholedate, taskDict=tasksDictionary))'''
        with zipfile.ZipFile(latexFiles, "a", zipfile.ZIP_DEFLATED, False) as zf:
            with user.team.dbConnect() as connection:
                dateList = self.entries.getDateList(connection)
                for dateString in dateList:
                    tasksDictionary = self.entries.getDateTasksDictionary(dateString, connection, smugmugConfig)
                    monthName = datetime.date(2020, int(dateString[5:-3]), 1).strftime('%B')
                    wholedate = monthName + " " + dateString[-2:]

        return static.serve_file(latexFiles, 'application/x-download','entryTex')



if __name__ == "__main__":
    smugmugConfig = json.load(open('secrets.json', 'r'))
    cherrypy.quickstart(FtcNotebook(), config='development.conf')
