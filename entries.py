import yaml
import os
import sqlite3
import uuid
import json
import smugmug
import datetime

class Entry():
    def __init__(self, date, taskName, memberName, accomplished, learned, nextSteps, photo):
        self.date = date
        self.taskName = taskName
        self.memberName = memberName
        self.accomplished = accomplished
        self.learned = learned
        self.nextSteps = nextSteps
        self.photo = photo
    
    def __str__(self):
        return f"Date: {self.date} Task: {self.taskName} Member: {self.memberName}"

    def getPhotoLink(self, config):
        return smugmug.get_medium_link(self.photo, config)
        
class Entries():
    def createTable(self, dbConnection):
        dbConnection.execute("""
        CREATE TABLE Entries(
            id INTEGER PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            task_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            accomplished TEXT,
            learned TEXT,
            next_steps TEXT,
            photo TEXT)""")


    def addEntry(self, dbConnection, date, taskId, memberId, accomplished, learned, nextSteps, photo):

        dbConnection.execute("Insert INTO Entries (date, task_id, member_id, accomplished, learned, next_steps, photo) VALUES (?,?,?,?,?,?,?)", (date, taskId, memberId, accomplished, learned, nextSteps, photo))

    def migrate(self, dbConnection, dbSchemaVersion):
        pass

    def getDateList(self, dbConnection):
        dateList = []
        for row in dbConnection.execute("SELECT date FROM Entries"):
            print(row[0])
            newDate = row[0].strftime("%Y-%m-%d")
            if newDate not in dateList:
                dateList.append(newDate)

        
        return dateList

    def getDateTasksDictionary(self, dateStr, dbConnection):
        dateParts = dateStr.split("-")
        date = datetime.datetime(int(dateParts[0]), int(dateParts[1]), int(dateParts[2]))
        beginTimeStamp = date.replace(hour = 0, minute=0, second=0)
        endTimeStamp = date.replace(hour = 23, minute=59, second=59)
        entryDict = {}
        for row in dbConnection.execute("""
           SELECT tasks.name, members.name, accomplished, learned, next_steps, photo
           FROM Entries
           INNER JOIN tasks
            ON Entries.task_id = Tasks.id
           INNER JOIN members
            ON Entries.member_id = Members.id
           WHERE (date BETWEEN ? AND ?)       
            """,(beginTimeStamp, endTimeStamp)):
            newEntry = Entry(date, row[0], row[1], row[2], row[3], row[4], row[5])
            if not(row[0] in entryDict.keys()):
                entryDict[row[0]] = [newEntry]
            else:
                entryDict[row[0]].append(newEntry)
        return entryDict
    
    



if __name__ == "__main__":
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'data/testDatabase.sqlite3')
    
    # try:
    #     os.remove(DEFAULT_PATH)
    # except IOError:
    #     pass #delete File, if it doesn't exist we don't care

    
    with sqlite3.connect(DEFAULT_PATH) as connection:
        entries = Entries()
        #entries.createTable(connection)
        entries.addEntry(connection, datetime.datetime.now(), 2, 1, "Hi", "Saying Hi is fun", "Say Hi to more people", "")
        entriesDict = entries.getDateTasksDictionary(datetime.datetime.now(), connection)
        for k, v in entriesDict.items():
            print(k + ":")
            for entry in v:
                print("-", entry)
        

# if __name__ == "__main__":
#     Entry = Minutes('data/9.8.2019.yaml')
#     Entry.toHtml()