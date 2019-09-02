import yaml
import uuid

class Minutes():
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        try:
            file = open(self.filename)
            yamlData = yaml.load(file)
            if type(yamlData) == list:
                self.entries = yamlData
        except FileNotFoundError:
            pass
        
    def addEntry(self, team_member, task, accomplished, learning, next_steps, photo):
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


        with open(self.filename, "w") as file:
            print(yaml.dump(self.entries))
            yaml.dump(self.entries, file,sort_keys=False)

if __name__ == "__main__":
    Entry = Minutes('data/9.2.2019.yaml')
    Entry.addEntry("Testerman", "testing", "accomplished testing", "learned testing", "next steps are to test", "This should be a link to a photo")