class Parameter:
    def __init__(self, number, mode):
        self.number = number
        self.mode = mode

    def getValue(self, listie):
        if self.mode == 0:
            return listie[self.number]
        if self.mode == 1:
            return self.number


def handleMult(index, command, list):
    modes = command.zfill(2)
    parameter1 = Parameter(list[index + 1], int(modes[-1]))
    parameter2 = Parameter(list[index + 2], int(modes[-2]))
    list[list[index + 3]] = parameter1.getValue(list) * parameter2.getValue(list)
    readmachead(index + 4, list)


def handleInp(index, list):
    list[list[index + 1]] = input
    readmachead(index + 2, list)


def handleOutp(index, list):
    output = list[list[index + 1]]
    print("output", output)
    readmachead(index + 2, list)

def handleSum(index, command, list):
    modes = command.zfill(2)
    parameter1 = Parameter(list[index + 1], int(modes[-1]))
    parameter2 = Parameter(list[index + 2], int(modes[-2]))
    list[list[index + 3]] = parameter1.getValue(list) + parameter2.getValue(list)
    readmachead(index + 4, list)


def handleJumpTrue(index, command, list):
    modes = command.zfill(2)
    parameter1 = Parameter(list[index + 1], int(modes[-1]))
    parameter2 = Parameter(list[index + 2], int(modes[-2]))
    if parameter1.getValue(list) != 0:
        readmachead(parameter2.getValue(list), list)
    else:
        readmachead(index + 3, list)

def handleJumpFalse(index, command, list):
    modes = command.zfill(2)
    parameter1 = Parameter(list[index + 1], int(modes[-1]))
    parameter2 = Parameter(list[index + 2], int(modes[-2]))
    if parameter1.getValue(list) == 0:
        readmachead(parameter2.getValue(list), list)
    else:
        readmachead(index + 3, list)

def lessThan(index, command, list):
    modes = command.zfill(3)
    parameter1 = Parameter(list[index + 1], int(modes[-1]))
    parameter2 = Parameter(list[index + 2], int(modes[-2]))
    if parameter1.getValue(list) < parameter2.getValue(list):
        list[list[index + 3]] = 1
    else:
        list[list[index + 3]] = 0
    readmachead(index + 4, list)

def equal(index, command, list):
    modes = command.zfill(3)
    parameter1 = Parameter(list[index + 1], int(modes[-1]))
    parameter2 = Parameter(list[index + 2], int(modes[-2]))
    if parameter1.getValue(list) == parameter2.getValue(list):
        list[list[index + 3]] = 1
    else:
        list[list[index + 3]] = 0
    readmachead(index + 4, list)



def readmachead(index, list):
    command = str(list[index])
    opcode = int(command[-2:])
    modes = command[:-2]
    if opcode == 99:
        return list
    if opcode == 1:
        handleSum(index, modes, list)
    if opcode == 2:
        handleMult(index, modes, list)
    if opcode == 3:
        handleInp(index, list)
    if opcode == 4:
        handleOutp(index, list)
    if opcode == 5:
        handleJumpTrue(index, modes, list)
    if opcode == 6:
        handleJumpFalse(index, modes, list)
    if opcode == 7:
        lessThan(index, modes, list)
    if opcode == 8:
        equal(index, modes, list)


input = 5
output = 99

with open("input.txt") as file:
    program = [int(entry) for entry in file.readline().split(",")]
print(readmachead(0, program))