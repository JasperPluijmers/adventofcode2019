def readmachead(index, list):
    commands = list[index:index+4]
    if commands[0] == 99:
        return list
    if commands[0] == 1:
        list[commands[3]] = list[commands[1]] + list[commands[2]]
        return readmachead(index + 4, list)
    if commands[0] == 2:
        list[commands[3]] = list[commands[1]] * list[commands[2]]
        return readmachead(index + 4, list)
    print("invalid program")

with open("input.txt") as file:
    input = [int(entry) for entry in file.readline().split(",")]

print("Answer for 1: ", readmachead(0, input.copy())[0])

for i in range(100):
    for j in range(100):
        inputModified = input.copy()
        inputModified[1:3] = [i,j]
        if (readmachead(0, inputModified)[0] == 19690720):
            print("Answer for 2:")
            print("i: ", i)
            print("j: ", j)
            print("100 * i + j: ", 100 * i + j)