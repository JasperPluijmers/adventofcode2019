import itertools
from enum import Enum
from typing import List, Dict
from abc import abstractmethod, ABC
import matplotlib.pyplot as plt
import numpy as np
import time

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

class OutputCollector(OutputDevice):
    output = []
    def receiveinput(self, param: int):
        self.output.append(param)
    def getandclearoutput(self):
        outputcopy = self.output.copy()
        self.output = []
        return outputcopy

class InputRenderer(InputDevice):
    outputdevice: OutputDevice = None
    def __init__(self, outputdevice):
        self.outputdevice = outputdevice

    def notify(self):
        updategameboard()
        output = None
        while not output in [-1,0,1]:
            try:
                output = int(input("Enter a number: "))
            except:
                print("Not a valid option")
        self.outputdevice.receiveinput(output)

class Inputai(InputDevice):
    outputdevice: OutputDevice = None
    def __init__(self, outputdevice):
        self.outputdevice = outputdevice

    def notify(self):
        time.sleep(0.05)
        updategameboard()
        draw()
        self.outputdevice.receiveinput(calculateposition())


def calculateposition():
    xpositionself = [tile.x for tile in gameboard if tile.block == tileType.HORPADDLE][-1]
    xpositionball = [tile.x for tile in gameboard if tile.block == tileType.BALL][-1]
    return np.sign(xpositionball - xpositionself)

currentscore = 0
def updategameboard():
    global currentscore
    collectedoutput = collector.getandclearoutput()
    boardlength = int(len(collectedoutput) / 3)
    newscore = 0
    for i in range(boardlength):
        values = collectedoutput[i * 3: (i * 3) + 3]
        if (values[0] == -1) & (values[1] == 0):
            newscore = values[2]
        else:
            newtile = GameTile(values[0], values[1], tileType(values[2]))
            gameboard.discard(newtile)
            gameboard.add(newtile)
    # sns.scatterplot([tile.x for tile in gameboard], [tile.y for tile in gameboard],
    #                  hue=[tile.block.value for tile in gameboard])
    # plt.show()
    if newscore > currentscore:
        currentscore = newscore

class tileType(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORPADDLE = 3
    BALL = 4

class GameTile:

    def __init__(self, x, y, block):
        self.x = x
        self.y = y
        self.block = block

    def __eq__(self, other):
        if isinstance(other, GameTile):
            return (self.x == other.x) & (self.y == other.y)

    def __hash__(self):
        return self.x.__hash__() + self.y.__hash__()

def draw():
    printstate = []
    for i in range(43):
        printstate.append([" "] * 43)
    for i in gameboard:
        printstate[i.y][i.x] = maptosymbol(i.block)
    print(chr(27) + "[2J")
    print("Score: " + str(currentscore))
    for line in printstate:
        print("".join(line))

def maptosymbol(tile):
    if tile == tileType.EMPTY:
        return " "
    if tile == tileType.WALL:
        return "#"
    if tile == tileType.BLOCK:
        return "x"
    if tile == tileType.HORPADDLE:
        return "_"
    if tile == tileType.BALL:
        return "O"

with open("input.txt") as file:
    program = [int(value) for value in file.readline().split(",")]

gameboard = set()
solver = OpcodeSolver(program)
renderer = Inputai(solver)
collector = OutputCollector()
solver.inputdevice = renderer
solver.outputdevice = collector
print([" "] * 43)
while solver.state != State.FINISHED:
    solver.readprogram()
print(len(gameboard))
print(len([value for value in collector.output[2::3] if value == 2]))
updategameboard()
print(currentscore)


# 14182 wrong