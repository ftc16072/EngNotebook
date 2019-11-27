import os
import sqlite3
import cherrypy
from mako.lookup import TemplateLookup
import yaml
import datetime
import glob
from minutes import Minutes
from tasks import Tasks, Task, TaskStages


DB_STRING = os.path.join(os.path.dirname(__file__), 'data\database.sqlite3')

class FtcNotebook(object):
    
    def __init__(self):
        self.lookup = TemplateLookup(directories = ['HtmlTemplates'], default_filters=['h'])
        self.tasks = Tasks()

    def template(self, template_name, **kwargs):
        return self.lookup.get_template(template_name).render(**kwargs)

    @cherrypy.expose
    def index(self):
        files = sorted(glob.iglob('data/[0-9]*.yaml'), reverse=True)
        return self.template('home.mako', files=files)

    @cherrypy.expose
    def newEntry(self):
        member_list = yaml.safe_load(open("data/members.yaml"))
        with sqlite3.connect(DB_STRING) as connection:
            taskList = self.tasks.getWorkingTaskList(connection)
        return self.template('engNotebookForm.mako', members=member_list, tasks=taskList)

    @cherrypy.expose
    def addEntry(self, Team_member, Task, Accomplished, Learning, Next_steps, Photo):
        print("Photo", Photo)
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        Entry = Minutes('data/'+ date + '.yaml')
        Entry.addEntry(Team_member, Task, Accomplished, Learning, Next_steps, Photo)
        return self.newEntry()
    
    @cherrypy.expose
    def tasksForm(self):
        taskStages = TaskStages
        with sqlite3.connect(DB_STRING) as connection:
            taskList = self.tasks.getAllTaskList(connection)
        return self.template('tasksForm.mako', taskList=taskList, TaskStages=taskStages)

    @cherrypy.expose
    def updateTasks(self, **kwargs):
        taskdict = dict(**kwargs) 
        with sqlite3.connect(DB_STRING) as connection:
            for (k, v) in taskdict.items():
                self.tasks.changeState(connection, taskId=k, newState=v)
        return self.tasksForm()

    @cherrypy.expose
    def addTasks(self, task, stage):
        with sqlite3.connect(DB_STRING) as connection:
            self.tasks.addTask(dbConnection=connection,name=task, stage=stage)
        return self.tasksForm()

    @cherrypy.expose
    def viewEntry(self, filename, destination):
        files = sorted(glob.iglob('data/[0-9]*.yaml'), reverse=True)
        previousEntry = ''
        nextEntry = ''
        for file in files:
            if(file == filename):
                if(files.index(file) + 1 >= len(files)):
                    previousEntry = ""
                else:
                    previousEntry = files[files.index(file) + 1]

                if(files.index(file) <= 0):
                    nextEntry = ""
                else:
                    nextEntry = files[files.index(file) - 1]

        
        print(previousEntry)
        return self.template('viewEntry.mako', previousEntry=previousEntry, nextEntry=nextEntry, minutes=Minutes(filename), pageTitle=filename[5:-5], destination=destination)    
        # if destination == "Screen":
        #     return self.template('viewEntry.mako', minutes=Minutes(filename), pageTitle=filename[5:-5])    
        # else:
        #     return self.template('printerFriendly.mako', minutes=Minutes(filename), pageTitle=filename[5:-5])
cherrypy.quickstart(FtcNotebook(), config='development.conf')