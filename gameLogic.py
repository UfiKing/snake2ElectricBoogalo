import sqlite3

connection = sqlite3.connect("leaderboard.db")
cursor = connection.cursor()

state = 1
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

badApples = False
pacifist = False

mouseButtonUp = False

pauseGame = False

def getGameState():
    global pauseGame
    return pauseGame

def switchGameState():
    global pauseGame
    if pauseGame:
        pauseGame = False
    else:
        pauseGame = True


def getPacifist():
    global pacifist
    return pacifist

def setPacifist(newState):
    global pacifist
    pacifist = newState

def getBadApples():
    global badApples
    return badApples

def setBadApples(newState):
    global badApples
    badApples = newState

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
