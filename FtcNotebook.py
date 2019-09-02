import cherrypy
from mako.lookup import TemplateLookup
import yaml
import datetime
from minutes import Minutes

class FtcNotebook(object):
    
    def __init__(self):
        self.lookup = TemplateLookup(directories = ['HtmlTemplates'], default_filters=['h'])

    def template(self, template_name, **kwargs):
        return self.lookup.get_template(template_name).render(**kwargs)

    @cherrypy.expose
    def index(self):
        member_list = yaml.safe_load(open("data/members.yaml"))
        tasks = yaml.safe_load(open("data/tasks.yaml"))
        return self.template('form.mako', members=member_list, tasks=tasks)

    @cherrypy.expose
    def addEntry(self, Team_member, Task, Accomplished, Learning, Next_steps, Photo):
        print("Photo", Photo)
        now = datetime.datetime.now()
        date = str(now.month) + "." + str(now.day) +"."+ str(now.year)
        Entry = Minutes('data/9.2.2019.yaml')
        Entry.addEntry(Team_member, Task, Accomplished, Learning, Next_steps, Photo)
        return "Thanks!"
            
        
        

cherrypy.quickstart(FtcNotebook(), config='development.conf')