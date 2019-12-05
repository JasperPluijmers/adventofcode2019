def handleMult(index, command, list):
    params = parameters(index, list, command.zfill(2))
    list[list[index + 3]] = params[0] * params[1]
    readmachead(index + 4, list)


def handleInp(index, list):
    list[list[index + 1]] = input
    readmachead(index + 2, list)


def handleOutp(index, list):
    output = list[list[index + 1]]
    print("output", output)
    readmachead(index + 2, list)

def handleSum(index, command, list):
    params = parameters(index, list, command.zfill(2))
    list[list[index + 3]] = params[0] + params[1]
    readmachead(index + 4, list)


def handleJumpTrue(index, command, list):
    params = parameters(index, list, command.zfill(2))
    if params[0] != 0:
        readmachead(params[1], list)
    else:
        readmachead(index + 3, list)

def handleJumpFalse(index, command, list):
    params = parameters(index, list, command.zfill(2))
    if params[0] == 0:
        readmachead(params[1], list)
    else:
        readmachead(index + 3, list)

def lessThan(index, command, list):
    params = parameters(index, list, command.zfill(3))
    if params[0] < params[1]:
        list[list[index + 3]] = 1
    else:
        list[list[index + 3]] = 0
    readmachead(index + 4, list)

def equal(index, command, list):
    params = parameters(index, list, command.zfill(3))
    if params[0] == params[1]:
        list[list[index + 3]] = 1
    else:
        list[list[index + 3]] = 0
    readmachead(index + 4, list)

def parameters(index, list, modes):
    parameterlist = []
    for i in range(1, len(modes) + 1):
        if int(modes[-i]) == 0:
            parameterlist.append(list[list[index + i]])
        elif int(modes[-i]) == 1:
            parameterlist.append(list[index + i])
    return parameterlist


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