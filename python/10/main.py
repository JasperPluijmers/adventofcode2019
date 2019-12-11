import math
from collections import Counter
from itertools import cycle

def GetAngleDegree(origin,target):
    n = -90 + (math.atan2(origin.y - target.y, origin.x - target.x)) * 180 / math.pi
    return n % 360


def distance(origin, target):
    return math.sqrt((origin.x - target.x)**2 + (origin.y - target.y)**2)


class relativeasteroid():
    def __init__(self, angle, distance, asteroid):
        self.angle = angle
        self.distance = distance
        self.asteroid = asteroid

    def __repr__(self):
        return self.asteroid.__repr__() + " and distance: " + str(self.distance) + " And angle: " + str(self.angle)
class Asteroid():

    def canseeamount(self, allasteroids):
        usableasteroids = allasteroids.copy()
        usableasteroids.remove(self)
        angles = map(lambda otherasteroid: GetAngleDegree(self, otherasteroid), usableasteroids)
        return len(set(angles))

    def allangles(self, allasteroids):
        usableasteroids = allasteroids.copy()
        usableasteroids.remove(self)
        return map(lambda otherasteroid: GetAngleDegree(self, otherasteroid), usableasteroids)

    def allanglesasteroids(self, allasteroids):
        usableasteroids = allasteroids.copy()
        usableasteroids.remove(self)
        return map(lambda otherasteroid: relativeasteroid(GetAngleDegree(self, otherasteroid), distance(self, otherasteroid), otherasteroid), usableasteroids)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Asteroid at: " + str(self.x) + ", " + str(self.y)

    def __eq__(self, other):
        if isinstance(other, Asteroid):
            return (self.x == other.x) & (self.y == other.y)

with open("input.txt") as file:
    asteroidfield = file.readlines()

asteroids = []
for y, row in enumerate(asteroidfield):
    for x, space in enumerate(row):
        if space == "#":
            asteroids.append(Asteroid(x, y))

maxseeing = max([asteroid.canseeamount(asteroids) for asteroid in asteroids])
print(maxseeing)
for i in asteroids:
    if i.canseeamount(asteroids) == maxseeing:
        base = i
        print(base)
asteroidcount = Counter(base.allangles(asteroids))
options = list(base.allanglesasteroids(asteroids))
options.sort(key=lambda x: x.distance)
print(options)

angleoptions = list(set(map(lambda x: x.angle, options)))
angleoptions.sort()
print(angleoptions)
angleoptions = cycle(angleoptions)
shot = 0

while shot < 200:
    currentangle = next(angleoptions)
    print(currentangle)
    nextplanet = next((planet for planet in options if planet.angle == currentangle), None)
    if nextplanet != None:
        print(str(shot) + " ) shooting angle: " + str(nextplanet))
        options.remove(nextplanet)
        shot = shot + 1
    else:
        print("nothing found")
