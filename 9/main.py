import itertools
from enum import Enum

class State(Enum):
    RUNNING = 0
    WAITING = 1
    FINISHED = 2

class opcodesolver:
    instructionpointer = 0
    relativebase = 0
    state = State.WAITING
    outputdevice = None

    def __init__(self, program, phase):
        self.program = program
        self.inputs = []
        self.inputs.append(phase)
        self.state = State.RUNNING

    def readprogram(self):
        command = str(self.program[self.instructionpointer])
        opcode = int(command[-2:])
        modes = command[:-2]
        if opcode == 99:
            self.state = State.FINISHED
            return
        if opcode == 1:
            self.handleSum(modes)
        if opcode == 2:
            self.handleMult(modes)
        if opcode == 3:
            self.handleInp(modes)
        if opcode == 4:
            self.handleOutp(modes)
        if opcode == 5:
            self.handleJumpTrue(modes)
        if opcode == 6:
            self.handleJumpFalse(modes)
        if opcode == 7:
            self.lessThan(modes)
        if opcode == 8:
            self.equal(modes)
        if opcode == 9:
            self.adjustrelbase(modes)
        if opcode not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]:
            print("error")

    def handleMult(self, command):
        params = self.parameters(command.zfill(2)[-2:])
        self.writetomemory(self.program[self.instructionpointer + 3], params[0] * params[1], command.zfill(3)[0] == "2")
        self.moveinstructionpointer(4)

    def handleInp(self, command):
        if len(self.inputs) == 0:
            self.state = State.WAITING
            return
        self.writetomemory(self.program[self.instructionpointer + 1], self.inputs[0], command.zfill(1)[0] == "2")
        self.inputs.pop(0)
        self.moveinstructionpointer(2)

    def handleOutp(self, modes):
        modes = modes.zfill(1)
        if (int(modes[-1])) == 0:
            self.giveOutput(self.program[self.program[self.instructionpointer + 1]])
        if (int(modes[-1])) == 1:
            self.giveOutput(self.program[self.instructionpointer + 1])
        if int(modes[-1]) == 2:
            self.giveOutput(self.program[self.relativebase + self.program[self.instructionpointer + 1]])
        self.moveinstructionpointer(2)

    def handleSum(self, command):
        params = self.parameters(command.zfill(2)[-2:])
        self.writetomemory(self.program[self.instructionpointer + 3], params[0] + params[1], command.zfill(3)[0] == "2")
        self.moveinstructionpointer(4)

    def handleJumpTrue(self, command):
        params = self.parameters(command.zfill(2))
        if params[0] != 0:
            self.setinstructionpointer(params[1])
        else:
            self.moveinstructionpointer(3)

    def handleJumpFalse(self, command):
        params = self.parameters(command.zfill(2))
        if params[0] == 0:
            self.setinstructionpointer(params[1])
        else:
            self.moveinstructionpointer(3)

    def lessThan(self, command):
        params = self.parameters(command.zfill(3))
        if params[0] < params[1]:
            self.writetomemory(self.program[self.instructionpointer + 3], 1, command.zfill(3)[0] == "2")
        else:
            self.writetomemory(self.program[self.instructionpointer + 3], 0, command.zfill(3)[0] == "2")
        self.moveinstructionpointer(4)

    def equal(self, command):
        params = self.parameters(command.zfill(3))
        if params[0] == params[1]:
            self.writetomemory(self.program[self.instructionpointer + 3], 1, command.zfill(3)[0] == "2")
        else:
            self.writetomemory(self.program[self.instructionpointer + 3], 0, command.zfill(3)[0] == "2")
        self.moveinstructionpointer(4)

    def parameters(self, modes):
        parameterlist = []
        for i in range(1, len(modes) + 1):
            if int(modes[-i]) == 0:
                if len(self.program) < self.program[self.instructionpointer + i] + i:
                    parameterlist.append(0)
                else:
                    parameterlist.append(self.program[self.program[self.instructionpointer + i]])
            elif int(modes[-i]) == 1:
                    parameterlist.append(self.program[self.instructionpointer + i])
            elif int(modes[-i]) == 2:
                parameterlist.append(self.program[self.relativebase + self.program[self.instructionpointer + i]])
        return parameterlist

    def moveinstructionpointer(self, amount):
        self.instructionpointer += amount

    def giveOutput(self, param):
        self.outputdevice.receiveInput(param)

    def receiveInput(self, param):
        self.inputs.append(param)
        if (self.state == State.WAITING):
            self.state = State.RUNNING

    def setinstructionpointer(self, param):
        self.instructionpointer = param

    def adjustrelbase(self, modes):
        params = self.parameters(modes.zfill(1))
        self.relativebase += params[0]
        self.moveinstructionpointer(2)

    def writetomemory(self, position, value, isrelative):
        if isrelative:
            position = position + self.relativebase
        if len(self.program) <= position:
            n = position - len(self.program) + 1
            self.program = self.program + ([0] * n)
        self.program[position] = value

class Outputprinter():
    def receiveInput(self, param):
        print("received input:" + str(param))

with open("input.txt") as file:
    program = [int(entry) for entry in file.readline().split(",")]

programs = []
outputs = []

programrunner = opcodesolver(program,2)
programrunner.outputdevice = Outputprinter()
while programrunner.state != State.FINISHED:
    programrunner.readprogram()


