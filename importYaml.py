import yaml
import sqlite3
import os
import glob
import datetime
import json

from tasks import Tasks, TaskStages
from members import Members
from entries import Entries

def textToStage(stageString):
    if stageString == "Working On":
        return TaskStages.workingOn
    if stageString == "Completed":
        return TaskStages.completed
    if stageString == "Abandoned":
        return TaskStages.abandoned

    return TaskStages.workingOn

if __name__ == "__main__":
    DB_STRING = os.path.join(os.path.dirname(__file__), 'data/database.sqlite3')
    
    try:
        os.remove(DB_STRING)
    except IOError:
        pass #delete File, if it doesn't exist we don't care

    with sqlite3.connect(DB_STRING) as connection:
        tasks = Tasks()
        members = Members()
        entries = Entries()
        smugmugConfig =  json.load(open('secrets.json', 'r'))

        #Create the Tables
        tasks.createTable(connection)
        members.createTable(connection)
        entries.createTable(connection)

        #Initate our Members Table
        membersList = ["Andrew Vo", "Chirag Sreedhara", "Eric Wong", "Evan Spiering", "Izaak Kreykes", "Nithya Golla", "Philip Smith", "Preeti Thirukonda", "Rishi Maroju"]
        members.insertMembers(connection, membersList)

        #Pull the Tasks over
        taskList = yaml.safe_load(open("data/tasks.yaml"))
        for task in taskList:
            tasks.addTask(connection, task['name'], textToStage(task['stage']))

        #flip the Entries
        files = sorted(glob.iglob('data/[0-9]*.yaml'), reverse=True)
        for file in files:
            date = file[5:-5]
            entryList = yaml.safe_load(open(file))
            for entry in entryList:
                print(tasks.getTaskId(connection, entry['task']), members.getTaskId(connection, entry['team_member']), entry['accomplished'], entry['learning'], entry['next_steps'], entry['photo'])
                entries.addEntry(connection, date, tasks.getTaskId(connection, entry['task']), members.getTaskId(connection, entry['team_member']), entry['accomplished'], entry['learning'], entry['next_steps'], entry['photo'], smugmugConfig)
                print("----------------------------------------")
        
        # now = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # entries.addEntry(connection, now, 1, 1, "accomplished", "learning", "next_steps", "",  smugmugConfig)
        # entries.addEntry(connection, now, 2, 2, "accomplished", "learning", "next_steps", "",  smugmugConfig)
        # older = "2019-11-10"
        # entries.addEntry(connection, older, 1, 1, "accomplished", "learning", "next_steps", "", smugmugConfig)
        # tasks.addTask(connection, "Test", TaskStages.workingOn)
        # tasks.addTask(connection, "Working", TaskStages.workingOn)
