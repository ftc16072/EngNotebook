import sqlite3
import os

from entries import Entries
from members import Members
from tasks import Tasks

entries = Entries()
members = Members()
tasks = Tasks()

memberList = ["Andrew", "Chirag", "Eric", "Izaak", "Nithya", "Philip", "Preeti", "Rishi", "Arjun", "Ryan", "Nikhil"]

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'data/database.sqlite3')

try:
    os.remove(DEFAULT_PATH)
except IOError:
    pass #delete File, if it doesn't exist we don't care

with sqlite3.connect(DEFAULT_PATH) as connection:
    members.createTable(connection)
    members.insertMembers(connection, memberList)
    tasks.createTable(connection)
    entries.createTable(connection)
    


