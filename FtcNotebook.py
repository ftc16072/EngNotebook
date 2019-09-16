import cherrypy
from mako.lookup import TemplateLookup
import yaml
import datetime
import glob
from minutes import Minutes
from tasks import Tasks

class FtcNotebook(object):
    
    def __init__(self):
        self.lookup = TemplateLookup(directories = ['HtmlTemplates'], default_filters=['h'])

    def template(self, template_name, **kwargs):
        return self.lookup.get_template(template_name).render(**kwargs)

    @cherrypy.expose
    def index(self):
        return self.template('home.mako')

    @cherrypy.expose
    def newEntry(self):
        member_list = yaml.safe_load(open("data/members.yaml"))
        tasks = yaml.safe_load(open("data/tasks.yaml"))
        return self.template('engNotebookForm.mako', members=member_list, tasks=tasks)

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
        tasks = yaml.safe_load(open("data/tasks.yaml"))
        print(tasks)
        return self.template('tasksForm.mako', tasks=tasks)

    @cherrypy.expose
    def updateTasks(self, **kwargs):
        tasks = Tasks()
        taskdict = dict(**kwargs) 
        tasks.UpdateTasks(taskdict)
        return self.tasksForm()

    @cherrypy.expose
    def addTasks(self, task, stage):
        tasks = Tasks()
        if tasks.AddTasks(taskName=task, stage=stage):
            return self.tasksForm()
        else:
            return "Something Went Wrong <br> <a href=addTasksForm>submit another</a> <br> <a href=tasksForm>Back</a>"

    @cherrypy.expose
    def viewEntries(self):
        files = sorted(glob.iglob('data/[0-9]*.yaml'))
        return self.template('veiwEntries.mako', files=files)

    @cherrypy.expose
    def viewEntry(self, filename):
        return self.template('viewEntry.mako', minutes=Minutes(filename), pageTitle=filename[5:-5])
        
        

cherrypy.quickstart(FtcNotebook(), config='development.conf')