def calculatefuel(mass):
    if (int(mass/3) - 2) < 0:
        return 0
    return int(mass/3) - 2

def calculatefuelextra(massExtra):
    if massExtra <= 0:
        return 0
    else:
        return calculatefuel(massExtra) + calculatefuelextra(calculatefuel(massExtra))

total = 0

with open("input.txt") as file:
    for massModule in file.readlines():
        total += calculatefuelextra(int(massModule))

print(total)
