import json

with open("settings.json", "r") as file:
    file = json.load(file)

cellSize = file["cell"]["size"]
cellNumber = file["cell"]["number"]
canQuit = file["canQuit"]
if type(cellSize) != int:
    raise ValueError(f"Invalid cellSize type, expected {int} but got {type(cellSize)}")
if type(cellNumber) != int:
    raise ValueError(f"Invalid cellNumber type, expected {int} but got {type(cellNumber)}")
if type(canQuit) != int:
    raise ValueError(f"Invalid canQuit type, expected {int} but got {type(canQuit)}")
if canQuit == 1:
    canQuit = True
elif canQuit == 0:
    canQuit = False
else:
    raise ValueError(f"Invalid canQuit value, expected: 1 or 0, but got {canQuit}")