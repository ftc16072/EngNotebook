from users import Users
from members import Members
from team import Team
import smugmug

USER_NAME = "alan@randomsmiths.com"
TEAM_NAME = "ftc16072"
PASSWORD = "password"

membersList = [
    "Andrew", "Chirag", "Eric", "Izaak", "Nithya", "Philip", "Preeti", "Rishi",
    "Arjun", "Ryan", "Nikhil"
]
albumDict = {
    '2019-04-01': '/api/v2/album/VgQcSw',
    '2020-03-01': '/api/v2/album/2z78cj'
}

if __name__ == "__main__":
    users = Users()
    members = Members()
    team = Team(TEAM_NAME)
    users.add(USER_NAME, TEAM_NAME, PASSWORD)
    user = users.getUser(USER_NAME, PASSWORD)
    with user.team.dbConnect() as connection:
        members.createTable(connection)
        members.insertMembers(connection, membersList)
        smugmug.createTable(connection)
        for date, album in albumDict:
            smugmug.addEntry(connection, date, album)
