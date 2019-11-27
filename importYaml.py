import yaml
import sqlite3
import os

from tasks import Tasks, TaskStages
from members import Members


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
