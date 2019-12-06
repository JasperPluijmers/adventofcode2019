class Planet:
    def __init__(self, id, orbitee):
        self.id = id
        self.orbitee = orbitee

    def orbitcount(self):
        count = 0
        nextorbitee = self.orbitee
        while (nextorbitee != None):
            count += 1
            nextorbitee = nextorbitee.orbitee
        return count

    def orbits(self):
        planets = []
        nextorbitee = self.orbitee
        while (nextorbitee != None):
            planets.append(nextorbitee)
            nextorbitee = nextorbitee.orbitee
        return planets

    def __eq__(self, other):
        if isinstance(other, Planet):
            return self.id == other.id

    def __hash__(self):
        return self.id.__hash__()

    def __repr__(self):
        return "Planet: " + str(self.id)

with open("input.txt") as file:
    input = [entry.strip().split(")") for entry in file.readlines()]

planets = []

for orbitee, orbiter in input:
    if (Planet(orbitee, None) in planets):
        orbitee = list(filter(lambda planet: planet.id == orbitee, planets))[0]
    else:
        orbitee = Planet(orbitee, None)
        planets.append(orbitee)
    if (Planet(orbiter, None) in planets):
        orbiter = list(filter(lambda planet: planet.id == orbiter, planets))[0]
        orbiter.orbitee = orbitee
    else:
        planets.append(Planet(orbiter, orbitee))

print(sum([planet.orbitcount() for planet in planets]))
yourorbits = set(list(filter(lambda planet: planet.id == "YOU", planets))[0].orbits())
santaorbits = set(list(filter(lambda planet: planet.id == "SAN", planets))[0].orbits())
print(len(yourorbits.symmetric_difference(santaorbits)))