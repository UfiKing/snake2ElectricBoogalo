import sqlite3

connection = sqlite3.connect("leaderboard.db")
cursor = connection.cursor()

state = 4
# these are the possible game states
# 1 -> mainMenu
# 2 -> game
# 3 -> gameOver
# 4 -> nameEntryScreen
# 5 -> leaderBoard

previousState = state
name = "anon"
id = 1
mode = 2
# modes:
# - 1: default
# - 2: bad apples

def addToDB(inputName, score):
    data = [inputName, score]

    cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", data)
    connection.commit()


def updateDB(id, score):
    data = [score, id]
    cursor.execute("UPDATE leaderboard SET score=? WHERE id=?", data)
    connection.commit()


def getLeaderboard():
    result = cursor.execute("SELECT * FROM leaderboard ORDER BY score DESC limit 10").fetchall()
    return result


def getTopId():
    ids = cursor.execute("SELECT * FROM leaderboard ORDER BY id DESC limit 10").fetchall()
    return ids[0][0]

def changeState(newState):
    global state
    global previousState
    previousState = state
    state = newState
    getLeaderboard()
    #print(state)

def changeUsername(newUsername):
    global name
    name = newUsername

def getUsername():
    global name
    return name

def changeId(newId):
    global id
    id = newId

def getPreviousState():
    global previousState
    return previousState

def getState():
    global state
    return state