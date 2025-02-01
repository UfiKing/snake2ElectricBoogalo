import json

with open("settings.json", "r") as file:
    file = json.load(file)

cellSize = file["cell"]["size"]
cellNumber = file["cell"]["number"]

if type(cellSize) != int:
    raise ValueError(f"Invalid cellSize type, expected {int} but got {type(cellSize)}")
if type(cellNumber) != int:
    raise ValueError(f"Invalid cellSize type, expected {int} but got {type(cellNumber)}")