import itertools
from enum import Enum

class State(Enum):
    RUNNING = 0
    WAITING = 1
    FINISHED = 2

class opcodesolver:
    instructionpointer = 0
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
            self.handleInp()
        if opcode == 4:
            self.handleOutp()
        if opcode == 5:
            self.handleJumpTrue(modes)
        if opcode == 6:
            self.handleJumpFalse(modes)
        if opcode == 7:
            self.lessThan(modes)
        if opcode == 8:
            self.equal(modes)

    def handleMult(self, command):
        params = self.parameters(command.zfill(2))
        self.program[self.program[self.instructionpointer + 3]] = params[0] * params[1]
        self.moveinstructionpointer(4)

    def handleInp(self):
        if len(self.inputs) == 0:
            self.state = State.WAITING
            return
        self.program[self.program[self.instructionpointer + 1]] = self.inputs[0]
        self.inputs.pop(0)
        self.moveinstructionpointer(2)

    def handleOutp(self):
        self.giveOutput(self.program[self.program[self.instructionpointer + 1]])
        self.moveinstructionpointer(2)

    def handleSum(self, command):
        params = self.parameters(command.zfill(2))
        self.program[self.program[self.instructionpointer + 3]] = params[0] + params[1]
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
            self.program[self.program[self.instructionpointer + 3]] = 1
        else:
            self.program[self.program[self.instructionpointer + 3]] = 0
        self.moveinstructionpointer(4)

    def equal(self, command):
        params = self.parameters(command.zfill(3))
        if params[0] == params[1]:
            self.program[self.program[self.instructionpointer + 3]] = 1
        else:
            self.program[self.program[self.instructionpointer + 3]] = 0
        self.moveinstructionpointer(4)

    def parameters(self, modes):
        parameterlist = []
        for i in range(1, len(modes) + 1):
            if int(modes[-i]) == 0:
                parameterlist.append(self.program[self.program[self.instructionpointer + i]])
            elif int(modes[-i]) == 1:
                parameterlist.append(self.program[self.instructionpointer + i])
        return parameterlist

    def moveinstructionpointer(self, amount):
        self.instructionpointer += amount

    def giveOutput(self, param):
        print("giving output: ", param)
        self.outputdevice.receiveInput(param)

    def receiveInput(self, param):
        self.inputs.append(param)
        if (self.state == State.WAITING):
            self.state = State.RUNNING

    def setinstructionpointer(self, param):
        self.instructionpointer = param


with open("input.txt") as file:
    program = [int(entry) for entry in file.readline().split(",")]

programs = []
outputs = []
for combination in itertools.permutations([5,6,7,8,9]):
    for phase in combination:
        programs.append(opcodesolver(program.copy(), phase))
    programs[0].outputdevice = programs[1]
    programs[1].outputdevice = programs[2]
    programs[2].outputdevice = programs[3]
    programs[3].outputdevice = programs[4]
    programs[4].outputdevice = programs[0]
    programs[0].inputs.append(0)
    while(programs[4].state != State.FINISHED):
        for i in programs:
            if (i.state != State.FINISHED):
                i.readprogram()
    outputs.append(programs[0].inputs[0])
    programs = []
print(outputs)
print(max(outputs))

