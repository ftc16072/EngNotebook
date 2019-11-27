import os
import sqlite3
from enum import IntEnum

class TaskStages(IntEnum):
    workingOn = 0
    completed = 1
    abandoned = 2
        

class Task():
    def __init__(self, taskId, name, stage):
        self.taskId = taskId
        self.name = name
        self.stage = stage
    
    def __str__(self):
        return f"ID:{self.taskId} -- Name:{self.name} -- stage:{self.stage}"



class Tasks():
    def createTable(self, dbConnection):
        dbConnection.execute(
            """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            stage INTEGER NOT NULL DEFAULT 0)"""
            )

    def addTask(self, dbConnection, name, stage):
        dbConnection.execute("INSERT INTO tasks (name, stage) Values (?, ?)", (name, stage))
    
    def migrate(self, dbConnection, dbSchemaVersion):
        pass

    def changeState(self, dbConnection, taskId, newState):
        dbConnection.execute("UPDATE tasks SET stage = ? WHERE (id = ?)", (newState, taskId))

    def getAllTaskList(self, dbConnection):
        tasksList = []
        for row in dbConnection.execute("SELECT id, name, stage FROM tasks ORDER BY stage ASC, name ASC", ()):
            tasksList.append(Task(row[0], row[1], row[2]))
        return tasksList

    def getWorkingTaskList(self, dbConnection):
        tasksList = []
        for row in dbConnection.execute("SELECT id, name, stage FROM tasks WHERE stage = ? ORDER BY name ASC", (TaskStages.workingOn,)):
            tasksList.append(Task(row[0], row[1], row[2]))
        return tasksList


def printList(taskList):
    for task in taskList:
        print(task)

    print("----------------------")


if __name__ == "__main__":
    
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'data/testDatabase.sqlite3')
    
    try:
        os.remove(DEFAULT_PATH)
    except IOError:
        pass #delete File, if it doesn't exist we don't care

    
    with sqlite3.connect(DEFAULT_PATH) as connection:
        tasks = Tasks()

        tasks.createTable(connection)
        
        tasks.addTask(connection, "Test", TaskStages.workingOn)
        tasks.addTask(connection, "Working", TaskStages.workingOn)
        taskList = tasks.getAllTaskList(connection)
        printList(taskList)

        tasks.changeState(connection, 1, TaskStages.completed)
        taskList = tasks.getAllTaskList(connection)
        printList(taskList)
        
        taskList = tasks.getWorkingTaskList(connection)
        printList(taskList)