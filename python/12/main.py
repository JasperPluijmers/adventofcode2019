import numpy as np
import matplotlib.pyplot as plt


class State:
    state = np.array([])

    def __init__(self, moons):
        for moon in moons:
            self.state = np.concatenate((self.state, moon.velocity, moon.position))

    def __eq__(self, other):
        if isinstance(other, State):
            return np.array_equal(self.state, other.state)

    def __hash__(self):
        return (self.state).__hash__()

class Moon:
    velocity = np.zeros(3)

    def __init__(self, position):
        self.position = position

    def updatevelocity(self, othermoon):
        self.velocity = self.velocity + np.sign((- self.position + othermoon.position))

    def updateposition(self):
        self.position = self.position + self.velocity

    def calculateenergy(self):
        return np.sum(np.abs(self.velocity)) * np.sum(np.abs(self.position))

    def copy(self):
        mooncopy = Moon(np.copy(self.position))
        mooncopy.velocity = np.copy(self.velocity)
        return mooncopy

    def __eq__(self, other):
        if isinstance(other, Moon):

            return np.array_equal(self.velocity, other.velocity) & np.array_equal(self.position, other.position)

    def __hash__(self):
        return self.position.__hash__() + self.velocity.__hash__()

moons = [Moon(np.array([17, -7, -11])),
         Moon(np.array([1, 4, -1])),
         Moon(np.array([6, -2, -6])),
         Moon(np.array([19, 11, 9]))]


def getcoordinates(moonlist, coordinate):
    information = []
    for moon in moonlist:
        information.append(moon.position[coordinate])
        information.append(moon.velocity[coordinate])
    return information

def isdone():
    for i in indices:
        if len(i) == 0:
            return True
    return False

originalstate = [getcoordinates(moons, i) for i in range(3)]

indices = [[], [], []]
j = 0
while isdone():
    j += 1
    for moon in moons:
        for othermoon in moons:
            moon.updatevelocity(othermoon)
    for moon in moons:
        moon.updateposition()

    for i in range(3):
        if len(indices[i]) == 0:
            if getcoordinates(moons, i) == originalstate[i]:
                indices[i].append(j)


indices = [indice[0] for indice in indices]
print(indices)
print(np.lcm.reduce(indices))

