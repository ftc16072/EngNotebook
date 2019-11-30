import os
import sqlite3
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

        with self.dbConnect()  as connection:
            memberList = self.members.getMembers(connection)
            taskList = self.tasks.getWorkingTaskList(connection)
        return self.template('engNotebookForm.mako', members=memberList, tasks=taskList)

    @cherrypy.expose
    def addEntry(self, memberId, taskId, accomplished, learning, next_steps, photo):
        if photo.filename:
            imgKey = smugmug.upload_data(photo.filename, photo.file.read(), smugmugConfig)
        else:
            imgKey = ""

        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        with self.dbConnect()  as connection:
            self.entries.addEntry(connection, date, taskId, memberId, accomplished, learning, next_steps, imgKey, smugmugConfig)
        
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
        # for file in files:
        #     if(file == filename):
        #         if(files.index(file) + 1 >= len(files)):
        #             previousEntry = ""
        #         else:
        #             previousEntry = files[files.index(file) + 1]

        #         if(files.index(file) <= 0):
        #             nextEntry = ""
        #         else:
        #             nextEntry = files[files.index(file) - 1]
        with self.dbConnect() as connection:
            tasksDictionary = self.entries.getDateTasksDictionary(dateString, connection)

        return self.template('viewEntry.mako', previousEntry=previousEntry, nextEntry=nextEntry, tasksDictionary=tasksDictionary, pageTitle=dateString, destination=destination)    
        # if destination == "Screen":
        #     return self.template('viewEntry.mako', minutes=Minutes(filename), pageTitle=filename[5:-5])    
        # else:
        #     return self.template('printerFriendly.mako', minutes=Minutes(filename), pageTitle=filename[5:-5])

if __name__ == "__main__":
    cherrypy.quickstart(FtcNotebook(), config='development.conf')
    smugmugConfig = json.load(open('secrets.json', 'r'))