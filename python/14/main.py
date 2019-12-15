import math

class Material():
    ingredients = {}
    makeamount: int

    def __init__(self, ingredients, makeamount, name):
        self.ingredients = ingredients
        self.makeamount = makeamount
        self.name = name

    def getOre(self, amount, extramaterials):
        inreserve = 0
        if self in extramaterials:
            inreserve += extramaterials[self]
            if inreserve > amount:
                extramaterials[self] -= amount
                return 0
            extramaterials[self] -= inreserve
            if extramaterials[self] <= 0:
                extramaterials.pop(self)
        amount = amount - inreserve
        tomake = math.ceil((amount)/self.makeamount) * self.makeamount
        overproduce = tomake - amount
        if overproduce > 0:
            if self in extramaterials:
                extramaterials[self] += overproduce
            else:
                extramaterials[self] = overproduce
        oreneeded = 0
        for ingredient, ingredientamount in self.ingredients.items():
            if ingredient.name == "ORE":
                return tomake * ingredientamount / self.makeamount
            oreneeded += ingredient.getOre(tomake * ingredientamount / self.makeamount, extramaterials)
        return oreneeded



    def __eq__(self, other):
        if isinstance(other, Material):
            return (self.name == other.name)

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return "Material " + self.name

materials = []
with open("input.txt") as file:
    materialist = [line.strip().split(" => ") for line in file.readlines()]
    for eq in materialist:
        result = eq[1].split(" ")
        ingredients = eq[0].split(", ")
        newmaterial = next((material for material in materials if material.name == result[1]), Material({}, int(result[0]), result[1]))
        newmaterial.makeamount = int(result[0])
        materials.append(newmaterial)
        for ingredient in ingredients:
            ingredient = ingredient.split(" ")
            newingredient = next((material for material in materials if material.name == ingredient[1]),
                 Material({}, 1, ingredient[1]))
            newmaterial.ingredients[newingredient] = int(ingredient[0])
            materials.append(newingredient)

ingredients = {}
amount = 1000000000000
#10 000 000 is smaller
#20 000 000 is bigger
fuelmade = 1
print(next((material for material in materials if material.name == "FUEL")).getOre(1935265, ingredients))
for i in range(1935000,1935300):
    fuelmade = i
    if next((material for material in materials if material.name == "FUEL")).getOre(fuelmade, ingredients) > amount:
        print(fuelmade)
        break

print(ingredients)