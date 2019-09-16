import yaml
import uuid
import json
import smugmug

class Minutes():
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        self.config = json.load(open('secrets.json', 'r'))
        try:
            file = open(self.filename)
            yamlData = yaml.safe_load(file)
            print("---",yamlData)
            if type(yamlData) == list:
                self.entries = yamlData
        except FileNotFoundError:
            print(f'File Not Found: {filename}')
        
    def addEntry(self, team_member, task, accomplished, learning, next_steps, photo):
        if photo.filename:
           imgKey = smugmug.upload_data(photo.filename, photo.file.read(), self.config) 

           Entry = {
                'team_member':team_member,
                'task':task,
                'accomplished':accomplished,
                'learning':learning,
                'next_steps':next_steps,
                'photo':imgKey
           }
           self.entries.append(Entry)
        else:
            Entry = {
                'team_member':team_member,
                'task':task,
                'accomplished':accomplished,
                'learning':learning,
                'next_steps':next_steps,
                'photo': ''
            }
            self.entries.append(Entry)
 
        with open(self.filename, "w") as file:
            yaml.dump(self.entries, file,sort_keys=False)
    
    def getTasksDictionary(self):
        taskSorted = sorted(self.entries, key = lambda i: i['task'])
        tasksdict = {}
        for item in taskSorted:
            if not(item['task'] in tasksdict.keys()):
                tasksdict[item['task']] = [item]
            else:
                tasksdict[item['task']].append(item)
        
        return(tasksdict)
    def getPhotoLink(self, imgKey):
        return smugmug.get_medium_link(imgKey, self.config)


if __name__ == "__main__":
    Entry = Minutes('data/9.8.2019.yaml')
    Entry.toHtml()