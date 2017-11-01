from abc import ABC, abstractmethod
import numpy as np
import math


class Turtle(ABC):
    def __init__(self):
        self.position = (0, 0)
        self.angle = 90
        self.trace = []

    def move(self, step=1.0):
        # we could normalize direction
        x, y = self.position
        rad = self.angle * math.pi / 180.
        direction = (math.cos(rad), math.sin(rad))
        x += step * direction[0]
        y += step * direction[1]
        self.position = (x, y)

    def turn(self, degree):
        self.angle += degree

    def poop(self):
        self.trace.append(tuple(self.position))

    @abstractmethod
    def feed(self, symbol):
        pass

    def __call__(self, symbols):
        for symbol in symbols:
            self.feed(symbol)
        return self

    def numpy(self):
        return np.asarray(self.trace)



class FractalTree(Turtle):
    def __init__(self):
        super(FractalTree, self).__init__()
        self.stack = []

    def feed(self, symbol):
        if symbol == '0':
            # draw leaf
            self.move()
            self.poop()
        if symbol == '1':
            self.move()
            self.poop()
        elif symbol == '[':
            self.stack.append((self.position, self.angle))
            self.turn(-45)
        elif symbol == ']':
            self.position, self.angle = self.stack.pop()
            self.turn(45)


if __name__ == '__main__':
    from linsys import Lsys
    import matplotlib.pyplot as plt
    import sys
    n_iter = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print("N iter =", n_iter)
    fractal = Lsys({'1': '11', '0': '1[0]0'})
    turtle = FractalTree()
    symbols = fractal.apply('0', n_iter)
    print(len(symbols))
    trace = turtle(symbols).numpy()
    plt.figure(1)
    plt.scatter(trace[:, 0], trace[:, 1])
    plt.savefig('tree.png')
