import yaml
import os
import sqlite3
import uuid
import json
import smugmug
import datetime

class Entry():
    def __init__(self, date, taskName, memberName, accomplished, learned, nextSteps, photoLink):
        self.date = date
        self.taskName = taskName
        self.memberName = memberName
        self.accomplished = accomplished
        self.learned = learned
        self.nextSteps = nextSteps
        self.photoLink = photoLink
    
    def __str__(self):
        return f"Date: {self.date} Task: {self.taskName} Member: {self.memberName}"

    def getPhotoLink(self, config):
        return smugmug.get_medium_link(self.photo, config)
        
class Entries():
    def createTable(self, dbConnection):
        dbConnection.execute("""
        CREATE TABLE Entries(
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            task_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            accomplished TEXT,
            learned TEXT,
            next_steps TEXT,
            photo_link TEXT,
            imgKey TEXT)""")


    def addEntry(self, dbConnection, date, taskId, memberId, accomplished, learned, nextSteps, photo, smugmugConfig):
        
        dbConnection.execute("Insert INTO Entries (date, task_id, member_id, accomplished, learned, next_steps, imgKey) VALUES (?,?,?,?,?,?,?)", (date, taskId, memberId, accomplished, learned, nextSteps, photo))

    def migrate(self, dbConnection, dbSchemaVersion):
        pass

    def getDateList(self, dbConnection):
        dateList = []
        for row in dbConnection.execute("SELECT DISTINCT date FROM Entries ORDER BY date DESC"):
            dateList.append(row[0])

        return dateList

    def getPrevNext(self, dbConnection, dateString):
        dateList = self.getDateList(dbConnection)
        i = dateList.index(dateString)
        if i == len(dateList)-1:
            prev = ""
        else:
            prev = dateList[i + 1]
        if i == 0:
            next = ""
        else:
            next = dateList[i - 1]
        return (prev, next)

    def getDateTasksDictionary(self, dateStr, dbConnection, smugmugConfig):
        entryDict = {}
        for row in dbConnection.execute("""
           SELECT tasks.name, members.name, accomplished, learned, next_steps, photo_link, imgkey, Entries.id
           FROM Entries
           INNER JOIN tasks
            ON Entries.task_id = Tasks.id
           INNER JOIN members
            ON Entries.member_id = Members.id
           WHERE (date = ?)       
            """,(dateStr,)):
            if not(row[5]):
                if row[6]:
                    photoLink = smugmug.get_medium_link(row[6], smugmugConfig)
                    entryID = row[7]
                    print(entryID)
                    dbConnection.execute("""
                    UPDATE Entries
                    SET photo_link = ?
                    WHERE id = ?
                    """, (photoLink, entryID))
                    newEntry = Entry(dateStr, row[0], row[1], row[2], row[3], row[4], photoLink)
                else:
                    newEntry = Entry(dateStr, row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                newEntry = Entry(dateStr, row[0], row[1], row[2], row[3], row[4], row[5])
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
        entriesDict = entries.getDateTasksDictionary(datetime.datetime.now().strftime("%Y-%m-%d"), connection)
        for k, v in entriesDict.items():
            print(k + ":")
            for entry in v:
                print("-", entry)
        

# if __name__ == "__main__":
#     Entry = Minutes('data/9.8.2019.yaml')
#     Entry.toHtml()