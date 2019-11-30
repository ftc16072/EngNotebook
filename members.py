import os
import sqlite3

class Member():
    def __init__(self, memberId, name):
        self.memberId = memberId
        self.name = name
    def __str__(self):
        return f"ID:{self.memberId} -- Name:{self.name}"


class Members():
    def createTable(self, dbConnection):
        dbConnection.execute(
            """
        CREATE TABLE members (
            id integer PRIMARY KEY,
            name text NOT NULL)"""
            )

    def insertMembers(self, dbConnection, members):
        for member in members:
            dbConnection.execute("INSERT INTO members (name) Values (?)", (member,))
    
    def migrate(self, dbConnection, dbSchemaVersion):
        pass

    def getMembers(self, dbConnection):
        membersList = []
        for row in dbConnection.execute("SELECT id, name FROM members ORDER BY name ASC", ()):
            membersList.append(Member(row[0], row[1]))
        return membersList
        
    def getTaskId(self, dbconnection, memberText):
        return dbconnection.execute("SELECT id FROM members WHERE name = ?", (memberText,)).fetchone()[0]

def printList(memberList):
    for member in memberList:
        print(member)

    print("----------------------")

        
if __name__ == "__main__":
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'data/testDatabase.sqlite3')
    
    try:
        os.remove(DEFAULT_PATH)
    except IOError:
        pass #delete File, if it doesn't exist we don't care
    with sqlite3.connect(DEFAULT_PATH) as connection:
        members = Members()
        members.createTable(connection)
        membersList = ["Andrew Vo", "Chirag Sreedhara", "Eric Wong", "Evan Spiering", "Izaak Kreykes", "Nithya Golla", "Philip Smith", "Preeti Thirukonda", "Rishi Maroju"]
        members.insertMembers(connection, membersList)

        printList(members.getMembers(connection))
    