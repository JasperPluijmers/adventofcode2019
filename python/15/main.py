from enum import Enum
from typing import List, Dict
from abc import abstractmethod, ABC
import time
import seaborn as sns
import matplotlib.pyplot as plt

class State(Enum):
    RUNNING = 0
    WAITING = 1
    FINISHED = 2


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class OutputDevice(ABC):

    @abstractmethod
    def receiveinput(self, param: int):
        pass

class InputDevice(ABC):

    @abstractmethod
    def notify(self):
        pass


class Outputprinter(OutputDevice):

    def receiveinput(self, param: int):
        print("received input:" + str(param))

class ManualInput(InputDevice):
    outputdevice: OutputDevice = None
    def __init__(self, outputdevice):
        self.outputdevice = outputdevice
    def notify(self):
        self.outputdevice.receiveinput(int(input("enter a number:")))

class OpcodeSolver(OutputDevice):
    instructionpointer: int = 0
    relativebase: int = 0
    state: State = State.WAITING
    outputdevice: OutputDevice = Outputprinter()
    inputdevice: InputDevice = None
    program: List[int]
    inputs: List[int] = []

    def __init__(self, program: list):
        self.program = program
        self.state = State.RUNNING
        self.inputdevice = ManualInput(self)

    def readprogram(self):
        command = str(self.program[self.instructionpointer])
        opcode = int(command[-2:])
        modes = [ParameterMode(int(parameter)) for parameter in command[:-2].zfill(5)]
        if opcode == 99:
            self.state = State.FINISHED
            return
        elif opcode == 1:
            self.handleSum(modes)
        elif opcode == 2:
            self.handleMult(modes)
        elif opcode == 3:
            self.handleInp(modes)
        elif opcode == 4:
            self.handleOutp(modes)
        elif opcode == 5:
            self.handleJumpTrue(modes)
        elif opcode == 6:
            self.handleJumpFalse(modes)
        elif opcode == 7:
            self.lessThan(modes)
        elif opcode == 8:
            self.equal(modes)
        elif opcode == 9:
            self.adjustrelbase(modes)
        else:
            print("error, opcode unknown")
            exit()

    def handleMult(self, modes: List[ParameterMode]):
        params = self.parameters(modes, 2)
        self.writetomemory(self.program[self.instructionpointer + 3], params[0] * params[1], modes[-3])
        self.moveinstructionpointer(4)

    def handleInp(self, modes: List[ParameterMode]):
        if len(self.inputs) == 0:
            self.state = State.WAITING
            self.inputdevice.notify()
            return
        self.writetomemory(self.program[self.instructionpointer + 1], self.inputs[0], modes[-1])
        self.inputs.pop(0)
        self.moveinstructionpointer(2)

    def handleOutp(self, modes: List[ParameterMode]):
        params = (self.parameters(modes, 1))
        self.giveOutput(params[0])
        self.moveinstructionpointer(2)

    def handleSum(self, modes: List[ParameterMode]):
        params = self.parameters(modes, 2)
        self.writetomemory(self.program[self.instructionpointer + 3], params[0] + params[1], modes[-3])
        self.moveinstructionpointer(4)

    def handleJumpTrue(self, modes: List[ParameterMode]):
        params = self.parameters(modes, 2)
        if params[0] != 0:
            self.setinstructionpointer(params[1])
        else:
            self.moveinstructionpointer(3)

    def handleJumpFalse(self, modes: List[ParameterMode]):
        params = self.parameters(modes, 2)
        if params[0] == 0:
            self.setinstructionpointer(params[1])
        else:
            self.moveinstructionpointer(3)

    def lessThan(self, modes: List[ParameterMode]):
        params = self.parameters(modes, 2)
        if params[0] < params[1]:
            self.writetomemory(self.program[self.instructionpointer + 3], 1, modes[-3])
        else:
            self.writetomemory(self.program[self.instructionpointer + 3], 0, modes[-3])
        self.moveinstructionpointer(4)

    def equal(self, modes: List[ParameterMode]):
        params = self.parameters(modes, 2)
        if params[0] == params[1]:
            self.writetomemory(self.program[self.instructionpointer + 3], 1, modes[-3])
        else:
            self.writetomemory(self.program[self.instructionpointer + 3], 0, modes[-3])
        self.moveinstructionpointer(4)

    def parameters(self, modes: List[ParameterMode], amount: int) -> List[int]:
        parameterlist = []
        for i in range(1, amount + 1):
            if modes[-i] == ParameterMode.POSITION:
                if len(self.program) < self.program[self.instructionpointer + i] + i:
                    parameterlist.append(0)
                else:
                    parameterlist.append(self.program[self.program[self.instructionpointer + i]])
            elif modes[-i] == ParameterMode.IMMEDIATE:
                parameterlist.append(self.program[self.instructionpointer + i])
            elif modes[-i] == ParameterMode.RELATIVE:
                if len(self.program) < self.relativebase + self.program[self.instructionpointer + i]:
                    parameterlist.append(0)
                else:
                    parameterlist.append(self.program[self.relativebase + self.program[self.instructionpointer + i]])
        return parameterlist

    def moveinstructionpointer(self, amount: int):
        self.instructionpointer += amount

    def giveOutput(self, param: int):
        self.outputdevice.receiveinput(param)

    def receiveinput(self, param: int):
        self.inputs.append(param)
        if self.state == State.WAITING:
            self.state = State.RUNNING

    def setinstructionpointer(self, param: int):
        self.instructionpointer = param

    def adjustrelbase(self, modes: List[ParameterMode]):
        params = self.parameters(modes, 1)
        self.relativebase += params[0]
        self.moveinstructionpointer(2)

    def writetomemory(self, position: int, value: int, mode: ParameterMode):
        if mode == ParameterMode.RELATIVE:
            position = position + self.relativebase
        if len(self.program) <= position:
            n = position - len(self.program) + 1
            self.program = self.program + ([0] * n)
        self.program[position] = value

class Tiletype(Enum):
    Wall = 0
    Space = 1
    OxygenSystem = 2
    Player = 3
    Unknown = 4
    Origin = 5
    Oxygenated = 6

class Tile():
    def __init__(self, x, y, tiletype):
        self.x = x
        self.y = y
        self.tiletype = tiletype

    def moveto(self, tile):
        self.x = tile.x
        self.y = tile.y

    def __eq__(self, other):
        if isinstance(other, Tile):
            return (self.x == other.x) & (self.y == other.y)

    def __hash__(self):
        return self.x.__hash__() + self.y.__hash__()

    def __repr__(self):
        return "Position at: " + str(self.x) + ", " + str(self.y)

def typetosymbol(param):
    if param == Tiletype.Wall:
        return "#"
    if param == Tiletype.Space:
        return "."
    if param == Tiletype.Unknown:
        return " "
    if param == Tiletype.Player:
        return "@"
    if param == Tiletype.OxygenSystem:
        return "^"
    if param == Tiletype.Origin:
        return "O"
    if param == Tiletype.Oxygenated:
        return "*"


def render():
    xes = [tile.x for tile in io.knownpositions]
    yes = [tile.y for tile in io.knownpositions]
    types = [tile.tiletype for tile in io.knownpositions]
    ownposition = [io.currentposition.x - min(xes), io.currentposition.y - min(yes), io.currentposition.tiletype]
    zero = [min(xes), min(yes), Tiletype.Origin]
    xes = [tile.x - min(xes) for tile in io.knownpositions]
    yes = [tile.y - min(yes) for tile in io.knownpositions]
    field = []
    for i in range(max(yes) + 1):
        field.append([" "] * (max(xes) + 1))
    for i in range(len(xes)):
        field[yes[i]][xes[i]] = typetosymbol(types[i])
    field[ownposition[1]][ownposition[0]] = typetosymbol(ownposition[2])
    field[zero[1]][zero[0]] = typetosymbol(zero[2])
    for line in field:
        print("".join(line))

class OxygenFinder(InputDevice, OutputDevice):
    done = False
    currentposition = Tile(0, 0, Tiletype.Player)
    knownpositions = [Tile(0,0,Tiletype.Space)]
    lastposition: Tile
    history = [Tile(0,0,Tiletype.Space)]

    def notify(self):
        positions = self.surroundingtiles(self.currentposition)
        for index, tile in enumerate(positions):
            if tile.tiletype == Tiletype.Unknown:
                self.lastposition = tile
                self.outputdevice.receiveinput(index + 1)
                return
        self.moveback()

    def moveback(self):
        if len(self.history) == 0:
            self.done = True
            return
        movetotile = self.history[-1]
        self.history.pop(-1)
        self.lastposition = movetotile
        if self.currentposition.x - movetotile.x == 1:
            self.outputdevice.receiveinput(3)
            return
        if self.currentposition.x - movetotile.x == -1:
            self.outputdevice.receiveinput(4)
            return
        if self.currentposition.y - movetotile.y == 1:
            self.outputdevice.receiveinput(2)
            return
        if self.currentposition.y - movetotile.y == -1:
            self.outputdevice.receiveinput(1)
            return

    def receiveinput(self, param: int):
        if param == 1:
            self.history.append(self.lastposition)
            self.currentposition.moveto(self.lastposition)
        elif param == 2:
            print("FOUND THE OXYGEN THINGY ON: ", self.lastposition)
            self.history.append(self.lastposition)
            self.currentposition.moveto(self.lastposition)
        self.lastposition.tiletype = Tiletype(param)


    def surroundingtiles(self, tile):
        tiles = []
        tiles.append(self.getorcreate(tile.x , tile.y + 1))
        tiles.append(self.getorcreate(tile.x, tile.y - 1))
        tiles.append(self.getorcreate(tile.x - 1, tile.y))
        tiles.append(self.getorcreate(tile.x + 1,  tile.y))

        return tiles

    def getorcreate(self, x, y):
        tile = next((tile for tile in self.knownpositions if (tile.x == x) & (tile.y == y)), None)
        if tile == None:
            tile = Tile(x, y, Tiletype.Unknown)
            self.knownpositions.append(tile)
        return tile



with open("input.txt") as file:
    program = [int(entry) for entry in file.readline().split(",")]

solver = OpcodeSolver(program)
io = OxygenFinder()
solver.inputdevice = io
solver.outputdevice = io
io.outputdevice = solver
io.inputdevice = solver

while not io.done:
    solver.readprogram()
render()

for i in range(10000):
    oxygentiles = [tile for tile in io.knownpositions if (tile.tiletype == Tiletype.Oxygenated) | (tile.tiletype == Tiletype.OxygenSystem)]
    for tile in oxygentiles:
        surroundingtiles = io.surroundingtiles(tile)
        for surroundingtile in surroundingtiles:
            if surroundingtile.tiletype == Tiletype.Space:
                surroundingtile.tiletype = Tiletype.Oxygenated
    render()
    time.sleep(0.1)
    if len([tile for tile in io.knownpositions if tile.tiletype == Tiletype.Space]) == 0:
        print(i)
        break
render()