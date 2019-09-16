import yaml

class Tasks():
    def __init__(self):
        self.tasklist = []
        
    def UpdateTasks(self, tasks):

        for name, stage in tasks.items():
            taskformated = {
                'name': name, 
                'stage': stage
                }
            self.tasklist.append(taskformated)
            print(self.tasklist)
        with open("data/tasks.yaml", "w") as file:
            print(yaml.dump(sorted(self.tasklist, key = lambda i: i['stage'], reverse=True)))
            yaml.dump(sorted(self.tasklist, key = lambda i: i['stage'], reverse=True), file,sort_keys=False)

    def AddTasks(self, taskName, stage):
        try:
            file = open("data/tasks.yaml", "r")
            yamlData = yaml.load(file)
            self.tasklist = yamlData
            self.tasklist.append({'name':taskName, 'stage':stage})
            print("---",self.tasklist)
            fileWrite = open("data/tasks.yaml", "w")
            yaml.dump(sorted(self.tasklist, key = lambda i: i['stage'], reverse=True), fileWrite, sort_keys=False)
            return True
        except FileNotFoundError:
            return False


if __name__ == "__main__":
    Entry = Tasks()
    test = {'Test_1': 'Working On', 'Test_2': 'Working On', 'Test_3': 'Completed'}
    Entry.UpdateTasks(test)