import os
import sqlite3
import uuid
import json
import smugmug
import datetime
from tasks import Tasks, Task, TaskStages
from members import Members, Member

SCHEMA_VERSION = 8


class Entry():
    def __init__(self, date, taskName, memberName, hours, accomplished, why,
                 learned, nextSteps, notes, diagramDot, photoLink, imgKey):
        self.date = date
        self.taskName = taskName
        self.memberName = memberName
        self.accomplished = accomplished
        self.hours = hours
        self.why = why
        self.learned = learned
        self.nextSteps = nextSteps
        self.notes = notes
        self.diagramDot = diagramDot
        self.photoLink = photoLink
        self.imgKey = imgKey

    def __str__(self):
        return f"Date: {self.date} Task: {self.taskName} Member: {self.memberName}"

    def getPhotoLink(self, config):
        return smugmug.get_medium_link(self.imgKey, config)


class Entries():
    def __init__(self):
        self.tasks = Tasks()
        self.members = Members()
        self.SCHEMA_VERSION = SCHEMA_VERSION

    def createTable(self, dbConnection):
        dbConnection.execute("""
        CREATE TABLE Entries(
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            task_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            hours REAL,
            accomplished TEXT,
            why TEXT,
            learned TEXT,
            notes TEXT,
            diagramDot TEXT,
            next_steps TEXT,
            photo_link TEXT,
            imgKey TEXT)""")
        self.tasks.createTable(dbConnection)
        self.members.createTable(dbConnection)

        dbConnection.execute('PRAGMA schema_version = ' + str(SCHEMA_VERSION))

    def addEntry(self, dbConnection, date, taskId, memberId, hours,
                 accomplished, why, learned, nextSteps, notes, diagramDot,
                 photo, smugmugConfig):

        dbConnection.execute(
            "Insert INTO Entries (date, task_id, member_id, hours,accomplished, why, learned, next_steps, notes, diagramDot, imgKey) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (date, taskId, memberId, hours, accomplished, why, learned,
             nextSteps, notes, diagramDot, photo))

    def migrate(self, dbConnection, dbSchemaVersion):
        if dbSchemaVersion > SCHEMA_VERSION:
            raise Exception("Unknown DB schema version" + str(dbSchemaVersion))
        if dbSchemaVersion < 4:
            dbConnection.execute("ALTER TABLE Entries ADD why TEXT")
        if dbSchemaVersion < 5:
            dbConnection.execute("ALTER TABLE Entries ADD notes TEXT")
        if dbSchemaVersion < 6:
            dbConnection.execute("ALTER TABLE Entries ADD diagramDot TEXT")
        if dbSchemaVersion < 8:
            dbConnection.execute("ALTER TABLE Entries ADD hours REAL ")

        self.tasks.migrate(dbConnection, dbSchemaVersion)
        self.members.migrate(dbConnection, dbSchemaVersion)
        dbConnection.execute('PRAGMA schema_version = ' + str(SCHEMA_VERSION))

    def getDateList(self, dbConnection):
        dateList = []
        for row in dbConnection.execute(
                "SELECT DISTINCT date FROM Entries ORDER BY date DESC"):
            dateList.append(row[0])

        return dateList

    def getPrevNext(self, dbConnection, dateString):
        dateList = self.getDateList(dbConnection)
        i = dateList.index(dateString)
        if i == len(dateList) - 1:
            prev = ""
        else:
            prev = dateList[i + 1]
        if i == 0:
            next = ""
        else:
            next = dateList[i - 1]
        return (prev, next)

    def updateSmugmugLink(self, dbConnection, smugmugConfig, entryID, imgKey):
        photoLink = smugmug.get_medium_link(imgKey, smugmugConfig)
        dbConnection.execute(
            """
                    UPDATE Entries
                    SET photo_link = ?
                    WHERE id = ?
                    """, (photoLink, entryID))
        return photoLink

    def getDateTasksDictionary(self, dateStr, dbConnection, smugmugConfig):
        entryDict = {}
        for row in dbConnection.execute(
                """
           SELECT tasks.name, members.name, accomplished, why, learned, next_steps, notes, diagramDot, photo_link, imgkey, Entries.id, hours
           FROM Entries
           INNER JOIN tasks
            ON Entries.task_id = Tasks.id
           INNER JOIN members
            ON Entries.member_id = Members.id
           WHERE (date = ?)       
            """, (dateStr, )):
            taskName = row[0]
            memberName = row[1]
            accomplished = row[2]
            why = row[3]
            learned = row[4]
            next_steps = row[5]
            notes = row[6]
            diagramDot = row[7]
            photoLink = row[8]
            imgKey = row[9]
            entriesId = row[10]
            hours = row[11]

            if not (photoLink):
                if imgKey:
                    photoLink = self.updateSmugmugLink(dbConnection,
                                                       smugmugConfig,
                                                       entriesId, imgKey)
            newEntry = Entry(dateStr, taskName, memberName, hours,
                             accomplished, why, learned, next_steps, notes,
                             diagramDot, photoLink, imgKey)
            if not (row[0] in entryDict.keys()):
                entryDict[row[0]] = [newEntry]
            else:
                entryDict[row[0]].append(newEntry)

        return entryDict

    def getEntriesWithHours(self, dbConnection):
        entries = []
        for row in dbConnection.execute(
                """
           SELECT tasks.name, members.name, date, hours
           FROM Entries
           INNER JOIN tasks
            ON Entries.task_id = Tasks.id
           INNER JOIN members
            ON Entries.member_id = Members.id
           WHERE (hours > 0) ORDER BY date ASC
            """, ()):
            entries.append(
                Entry(date=row[2],
                      taskName=row[0],
                      memberName=row[1],
                      hours=row[3],
                      accomplished="",
                      why="",
                      learned="",
                      nextSteps="",
                      notes="",
                      diagramDot="",
                      photoLink="",
                      imgKey=""))
        return entries

    def getDateDictionary(self, taskId, dbConnection, smugmugConfig):
        entryDict = {}
        taskName = ""
        for row in dbConnection.execute(
                """
           SELECT tasks.name, members.name, accomplished, photo_link, imgkey, Entries.id, date, why, notes, diagramDot
           FROM Entries
           INNER JOIN tasks
            ON Entries.task_id = Tasks.id
           INNER JOIN members
            ON Entries.member_id = Members.id
           WHERE (Tasks.id = ?) ORDER BY date ASC
            """, (taskId, )):
            taskName = row[0]
            photoLink = row[3]
            imgKey = row[4]
            if not (photoLink):
                if imgKey:
                    photoLink = self.updateSmugmugLink(dbConnection,
                                                       smugmugConfig, row[5],
                                                       imgKey)
            newEntry = Entry(date=row[6],
                             taskName=taskName,
                             memberName=row[1],
                             hours=0,
                             accomplished=row[2],
                             learned="",
                             nextSteps="",
                             photoLink=photoLink,
                             imgKey=imgKey,
                             why=row[7],
                             notes=row[8],
                             diagramDot=row[9])
            if not (row[6] in entryDict.keys()):
                entryDict[row[6]] = [newEntry]
            else:
                entryDict[row[6]].append(newEntry)

        return (entryDict, taskName)


if __name__ == "__main__":
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__),
                                'data/testDatabase.sqlite3')

    # try:
    #     os.remove(DEFAULT_PATH)
    # except IOError:
    #     pass #delete File, if it doesn't exist we don't care
    """ 
    with sqlite3.connect(DEFAULT_PATH) as connection:
        entries = Entries()
        #entries.createTable(connection)
        entries.addEntry(connection, datetime.datetime.now(), 2, 1, "Hi", "Saying Hi is fun", "Say Hi to more people", "")
        entriesDict = entries.getDateTasksDictionary(datetime.datetime.now().strftime("%Y-%m-%d"), connection)
        for k, v in entriesDict.items():
            print(k + ":")
            for entry in v:
                print("-", entry)
         """

# if __name__ == "__main__":
#     Entry = Minutes('data/9.8.2019.yaml')
#     Entry.toHtml()
