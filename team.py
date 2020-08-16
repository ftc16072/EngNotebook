import re
import sqlite3
import os

from entries import Entries


def make_safe_name(input):
    return re.sub(r'\W+', '', input)


class Team(object):
    def __init__(self, teamName):
        self.teamName = teamName
        self.databaseName = 'data/' + make_safe_name(
            self.teamName) + '.sqlite3'
        self.entries = Entries()

        if not os.path.exists(self.databaseName):
            with self.dbConnect() as connection:
                self.entries.createTable(connection)

        with self.dbConnect() as connection:
            data = connection.execute("PRAGMA schema_version").fetchone()
            if data[0] != self.entries.SCHEMA_VERSION:
                self.entries.migrate(connection, data[0])

    def dbConnect(self):
        return sqlite3.connect(self.databaseName,
                               detect_types=sqlite3.PARSE_DECLTYPES)


class Teams(object):
    def __init__(self):
        self.teams = {}

    def getTeam(self, teamName):
        try:
            return self.teams[teamName]
        except KeyError:
            self.teams[teamName] = Team(teamName)
            return self.teams[teamName]


teams = Teams()
