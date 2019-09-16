import yaml
import uuid

class Minutes():
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        try:
            file = open(self.filename)
            yamlData = yaml.safe_load(file)
            print("---",yamlData)
            if type(yamlData) == list:
                self.entries = yamlData
        except FileNotFoundError:
            print(f'File Not Found: {filename}')
        
    def addEntry(self, team_member, task, accomplished, learning, next_steps, photo):
        print(photo.filename)
        if photo.filename:
            unique_filename = str(uuid.uuid4()) + photo.filename
            Entry = {
                'team_member':team_member,
                'task':task,
                'accomplished':accomplished,
                'learning':learning,
                'next_steps':next_steps,
                'photo':unique_filename
            }
            self.entries.append(Entry)
            print(self.entries)
            print(photo)
            with open("data/" + unique_filename, "wb") as outFile:
                while True:
                    data = photo.file.read(8192)
                    if not data:
                        break
                    outFile.write(data)
        else:
            Entry = {
                'team_member':team_member,
                'task':task,
                'accomplished':accomplished,
                'learning':learning,
                'next_steps':next_steps,
                'photo': 'Null'
            }
            self.entries.append(Entry)
            print(self.entries)

        with open(self.filename, "w") as file:
            print(yaml.dump(self.entries))
            yaml.dump(self.entries, file,sort_keys=False)
    
    def getTasksDictionary(self):
        taskSorted = sorted(self.entries, key = lambda i: i['task'])
        tasksdict = {}
        print('test')
        print(self.entries)
        for item in taskSorted:
            print(item)
            if not(item['task'] in tasksdict.keys()):
                tasksdict[item['task']] = [item]
            else:
                tasksdict[item['task']].append(item)
        
        return(tasksdict)
        


if __name__ == "__main__":
    Entry = Minutes('data/entries/9.8.2019.yaml')
    Entry.toHtml()