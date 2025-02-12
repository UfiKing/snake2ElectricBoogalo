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

numberOfApples = 1
isDead = False
previousState = state
name = "anon"
id = 1
mode = 1

# modes:
# - 0b0000: default
# - 0b0001: bad apples
# - 0b0010: 3 apples
# - 0b0100: 5 apples
# - 0b0011: 3 bad apples
# - 1: default
# - 2: bad apples
# - 3:

mouseButtonUp = False

def setDead():
    global isDead
    isDead = True

def setAlive():
    global isDead
    isDead = False

def getLivingState():
    global isDead
    return isDead

def setNumberOfApples(newNumberOfApples):
    global numberOfApples
    numberOfApples = newNumberOfApples

def getNumberOfApples():
    global numberOfApples
    return numberOfApples

def getMode():
    return mode

def changeMode(newMode):
    global mode
    mode = newMode


def getMouseButtonUp():
    return mouseButtonUp


def setMouseButtonUp(newState):
    global mouseButtonUp
    mouseButtonUp = newState


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
