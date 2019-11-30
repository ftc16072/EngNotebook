import yaml
import sqlite3
import os
import datetime

from tasks import Tasks, TaskStages
from members import Members
from entries import Entries


if __name__ == "__main__":
    DB_STRING = os.path.join(os.path.dirname(__file__), 'data/database.sqlite3')
    
    try:
        os.remove(DB_STRING)
    except IOError:
        pass #delete File, if it doesn't exist we don't care

    with sqlite3.connect(DB_STRING) as connection:
        tasks = Tasks()

        tasks.createTable(connection)
        
        tasks.addTask(connection, "Test", TaskStages.workingOn)
        tasks.addTask(connection, "Working", TaskStages.workingOn)

        members = Members()
        members.createTable(connection)
        membersList = ["Andrew Vo", "Chirag Sreedhara", "Eric Wong", "Evan Spiering", "Izaak Kreykes", "Nithya Golla", "Philip Smith", "Preeti Thirukonda", "Rishi Maroju"]
        members.insertMembers(connection, membersList)

        entries = Entries()
        entries.createTable(connection)
        now = datetime.datetime.now()
        entries.addEntry(connection, now, 1, 1, "accomplished", "learning", "next_steps", "")
        older = now.replace(month=11, day=12)
        entries.addEntry(connection, older, 1, 1, "accomplished", "learning", "next_steps", "")
