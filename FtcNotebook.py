import cherrypy
from mako.lookup import TemplateLookup
from yaml import load, dump

class FtcNotebook(object):
    
    def __init__(self):
        self.lookup = TemplateLookup(directories = ['HtmlTemplates'], default_filters=['h'])

    def template(self, template_name, **kwargs):
        return self.lookup.get_template(template_name).render(**kwargs)

    @cherrypy.expose
    def index(self):
        member_list = load(open("members.yaml"))
        print(member_list)
        tasks = ["test1", "Test2"]
        return self.template('form.mako', members=member_list, tasks=tasks)

    @cherrypy.expose
    def addEntry(self, Team_member, Task, Accomplished, Learning, Next_steps, Photo):
        return Team_member, Task, Accomplished, Learning, Next_steps, Photo

cherrypy.quickstart(FtcNotebook(), config='development.conf')