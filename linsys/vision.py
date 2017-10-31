from abc import ABC, abstractmethod
import numpy as np


class Turtle(ABC):
    def __init__(self):
        self.position = np.array([0., 0.])
        self.direction = np.array([0., 1.])
        self.trace = []

    def move(self, step=1.0):
        # we could normalize direction
        self.position += step * self.direction

    def poop(self):
        self.trace.append(tuple(self.position))

    @abstractmethod
    def feed(self, symbol):
        pass

    def __call__(self, symbols):
        for symbol in symbols:
            self.feed(symbol)
        return self


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
            self.stack.append((self.position.copy(), self.direction.copy()))
            self.direction += np.array([-1.4, 0.])  # turn left
        elif symbol == ']':
            self.position, self.direction = self.stack.pop()
            self.direction += np.array([1.4, 0.])  # turn right


if __name__ == '__main__':
    from linsys import Lsys
    import matplotlib.pyplot as plt
    fractal = Lsys({'1': '11', '0': '1[0]0'})
    turtle = FractalTree()
    symbols = fractal.apply('0', 7)
    turtle(symbols)
    trace = np.asarray(turtle.trace)
    plt.figure(1)
    plt.scatter(trace[:, 0], trace[:, 1])
    plt.savefig('tree.png')
