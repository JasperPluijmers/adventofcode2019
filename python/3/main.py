import matplotlib.pyplot as plt

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

with open("input.txt") as file:
    paths = [path.split(",") for path in file.readlines()]

points = [Point(0,0).pointsTouchedJourney(path) for path in paths]
pointset1 = set(points[0])
pointset2 = set(points[1])
intersect = pointset1.intersection(pointset2)
distancepoints = [point.distance() for point in intersect]
print(min(distancepoints[1:]))

wirelength = [points[0].index(intersection) + points[1].index(intersection) for intersection in intersect]
print(min(wirelength[1:]) + 2)

for pointsets in points:
    plt.plot([point.x for point in pointsets], [point.y for point in pointsets])

plt.show()