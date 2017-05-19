# This shows the first attempt at creating a predator prey scenario
# We build a board and populate it, no behavior or time-dependent actions happen yet

import random

import numpy as np
import matplotlib.pyplot as plt


class WorldGrid(object):

    def __init__(self, length=100, width=100):
        self.world = np.zeros((length, width), dtype=np.int)
        self.length = length
        self.width = width

    def populate(self, n, level=1):
        for _ in xrange(n):
            x_coord = random.randint(0, self.width-1)
            y_coord = random.randint(0, self.length-1)
            # TODO add a check here to make sure we are only populating zero spots
            self.world[x_coord][y_coord] = level

    def show_board(self):
        print "The board currently: \n"
        for line in xrange(self.length):
            print self.world[line]
        print "\n That is the board."

    def graph_board(self):
        plt.imshow(self.world, cmap='rainbow')
        plt.show()


def main():
    w = WorldGrid(100,100)
    w.populate(100)
    w.populate(50, level=2)
    w.populate(10, level=3)
    w.graph_board()

if __name__ == "__main__":
    main()