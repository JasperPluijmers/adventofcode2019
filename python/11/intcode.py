import itertools
from enum import Enum
from typing import List, Dict
from abc import abstractmethod, ABC


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

    def __init__(self, program: list, phase: int):
        self.program = program
        self.inputs.append(phase)
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

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pointsTouched(self, instruction):
        if (instruction[0] == "U"):
            return [Point(self.x, self.y + n) for n in range(1,int(instruction[1:]) + 1)]
        if (instruction[0] == "R"):
            return [Point(self.x + n, self.y) for n in range(1,int(instruction[1:]) + 1)]
        if (instruction[0] == "D"):
            return [Point(self.x, self.y - n) for n in range(1,int(instruction[1:]) + 1)]
        if (instruction[0] == "L"):
            return [Point(self.x - n, self.y) for n in range(1,int(instruction[1:]) + 1)]

    def pointsTouchedJourney(self, instructionList):
        currentPoint = self
        pointsTouchedList = []
        for instruction in instructionList:
            pointsTouchedList.extend(currentPoint.pointsTouched(instruction))
            currentPoint = pointsTouchedList[-1]
        return pointsTouchedList

    def distance(self):
        return abs(self.x) + abs(self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) & (self.y == other.y)

    def __hash__(self):
        return (self.x+self.y).__hash__()

    def __repr__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)

class Color(Enum):
    BLACK = 0,
    WHITE = 1

class Canvas():
    points: Dict[Point, Color] = {}

    def paintPoint(self, point, color):
        self.points[point] = color


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class PaintRobot(OutputDevice, InputDevice):
    inputs = []
    location: Point = Point(0,0)
    direction: Direction = Direction.NORTH
    canvas: Canvas = Canvas()
    computer: OutputDevice = None

    def receiveinput(self, param: int):
        self.inputs.append(param)
        if len(self.inputs) == 2:
            self.canvas.paintPoint(self.location, Color(self.inputs[0]))
            self.rotate(self.inputs[1])
            self.move(1)
            inputs = []

    def rotate(self, parameter: int):
        if parameter == 0:
            self.direction = Direction((self.direction.value - 1) % 4)
        if parameter == 1:
            self.direction = Direction((self.direction.value + 1) % 4)

    def move(self, amount):
        if self.direction == Direction.NORTH:
            self.location.y = self.location.y + 1
        if self.direction == Direction.WEST:
            self.location.x = self.location.x - 1
        if self.direction == Direction.SOUTH:
            self.location.y = self.location.y - 1
        if self.direction == Direction.EAST:
            self.location.x = self.location.x + 1

    def notify(self):
        self.computer.receiveinput(self.canvas.points[self.location].value)


