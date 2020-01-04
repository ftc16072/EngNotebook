import os
import sqlite3
import json
import cherrypy
from mako.lookup import TemplateLookup
import yaml
import datetime
import glob
from entries import Entries
from tasks import Tasks, Task, TaskStages
from members import Members, Member
import smugmug

smugmugConfig = {}
DB_STRING = os.path.join(os.path.dirname(__file__), 'data/database.sqlite3')

class FtcNotebook(object):
    
    def __init__(self):
        self.lookup = TemplateLookup(directories = ['HtmlTemplates'], default_filters=['h'])
        self.tasks = Tasks()
        self.members = Members()
        self.entries = Entries() 

    def dbConnect(self):
        return sqlite3.connect(DB_STRING, detect_types=sqlite3.PARSE_DECLTYPES)

    def template(self, template_name, **kwargs):
        return self.lookup.get_template(template_name).render(**kwargs)

    @cherrypy.expose
    def index(self):
        with self.dbConnect()  as connection:
            dateList = self.entries.getDateList(connection)
        
        return self.template('home.mako', dateList=dateList)

    @cherrypy.expose
    def newEntry(self):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        with self.dbConnect()  as connection:
            memberList = self.members.getMembers(connection)
            taskList = self.tasks.getWorkingTaskList(connection)
        return self.template('engNotebookForm.mako', dateString=date, members=memberList, tasks=taskList)

    @cherrypy.expose
    def addEntry(self, dateString, memberId, taskId, accomplished, learning, next_steps, photo):
        if photo.filename:
            imgKey = smugmug.upload_data(photo.filename, photo.file.read(), smugmugConfig)
        else:
            imgKey = ""

        with self.dbConnect()  as connection:
            self.entries.addEntry(connection, dateString, taskId, memberId, accomplished, learning, next_steps, imgKey, smugmugConfig)
        
        return self.newEntry()
    
    @cherrypy.expose
    def tasksForm(self):
        taskStages = TaskStages
        with self.dbConnect()  as connection:
            taskList = self.tasks.getAllTaskList(connection)
        return self.template('tasksForm.mako', taskList=taskList, TaskStages=taskStages)

    @cherrypy.expose
    def updateTasks(self, **kwargs):
        taskdict = dict(**kwargs) 
        with self.dbConnect()  as connection:
            for (k, v) in taskdict.items():
                self.tasks.changeState(connection, taskId=k, newState=v)
        return self.tasksForm()

    @cherrypy.expose
    def addTasks(self, task, stage):
        with self.dbConnect()  as connection:
            self.tasks.addTask(dbConnection=connection,name=task, stage=stage)
        return self.tasksForm()

    @cherrypy.expose
    def viewEntry(self, dateString, destination):
        previousEntry = ''
        nextEntry = ''
        
        with self.dbConnect() as connection:
            tasksDictionary = self.entries.getDateTasksDictionary(dateString, connection, smugmugConfig)
            (previousEntry, nextEntry) = self.entries.getPrevNext(connection, dateString)
        return self.template('viewEntry.mako', previousEntry=previousEntry, nextEntry=nextEntry, tasksDictionary=tasksDictionary, pageTitle=dateString, destination=destination)    

    @cherrypy.expose
    def viewTask(self, taskId):
        with self.dbConnect() as connection:
            (dateDictionary, taskName) = self.entries.getDateDictionary(taskId, connection, smugmugConfig)
        return self.template('viewTask.mako', dateDictionary=dateDictionary, pageTitle=taskName)
    
    @cherrypy.expose
    def viewTaskByName(self, taskName):
        with self.dbConnect() as connection:
            taskId = self.tasks.getTaskId(connection, taskName)
            (dateDictionary, taskName) = self.entries.getDateDictionary(taskId, connection, smugmugConfig)
        return self.template('viewTask.mako', dateDictionary=dateDictionary, pageTitle=taskName)
    

if __name__ == "__main__":
    smugmugConfig = json.load(open('secrets.json', 'r'))
    cherrypy.quickstart(FtcNotebook(), config='development.conf')
   