import numpy as np


class Layer:
    def __init__(self, pixels):
        self.pixels = pixels

    def count(self, number):
        amount = 0
        for pixel in self.pixels:
            if number == pixel:
                amount += 1
        return amount


class Picture:
    layers = []

    def __init__(self, pixels, layersize):
        for i in range(int(len(pixels)/layersize)):
            self.layers.append(Layer(pixels[i*layersize:(1+i)*layersize]))

    def pixellists(self):
        l = [layer.pixels for layer in self.layers]
        return [list(i) for i in zip(*l)]


with open("input.txt") as file:
    input = file.readline()

input = [int(c) for c in input]

picture = Picture(input, 25*6)

visiblepixels = [next(filter(lambda x: x != 2, pixellayers), 2) for pixellayers in picture.pixellists()]
print(np.reshape(visiblepixels, (6,25)))
print(min([layer.count(0) for layer in picture.layers]))
print([[layer.count(0), layer.count(1) * layer.count(2)] for layer in picture.layers])