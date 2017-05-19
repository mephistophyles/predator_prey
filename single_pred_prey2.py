# Building upon the previous file, we now modify the world grid to create creature objects that eat grass or each other

import copy
import random

import numpy as np
import matplotlib.pyplot as plt

WORLDLENGTH = 100 # y
WORLDWIDTH = 100 # x

class Creature(object):

    def __init__(self, length=WORLDLENGTH, width=WORLDWIDTH, level=2, hunger=5):
        self.x = random.randint(0, width-1)
        self.y = random.randint(0, length-1)
        self.level = level
        # later we can have creatures that compete for resources as well as subjective prey vulnerability
        self.eats = level-1
        # when hunger = 0, they die
        self.hunger = hunger
        # this difference lets me know if I need to check the creature list or worldmap for food
        if self.level == 2:
            self.vegetarian = True
        else:
            self.vegetarian = False

    def move(self):
        dx = random.randint(-2,2)
        dy = random.randint(-2,2)
        self.x = (self.x + dx)%WORLDWIDTH
        self.y = (self.y + dy)%WORLDLENGTH

    def update(self, world, creature_list):
        self.move()
        self.hunger -= 1
        if self.vegetarian:
            # info is the plainworld
            if world.world[self.x][self.y] == 1:
                self.hunger += 5
                world.world[self.x][self.y] = 0
        else:
            # info is the creature list
            for creature in creature_list:
                # predators can 'leap' to adjacent squares
                if abs(creature.x - self.x) < 2 and abs(creature.y - self.y) < 2 and creature.level == self.eats:
                    self.hunger += 5
                    creature_list.remove(creature)
        if self.hunger <= 0:
            creature_list.remove(self)

class WorldGrid(object):

    def __init__(self, length=WORLDLENGTH, width=WORLDWIDTH):
        self.world = np.zeros((length, width), dtype=np.int)
        self.length = length
        self.width = width

    def populate(self, n, level=1):
        for _ in xrange(n):
            x_coord = random.randint(0, self.width-1)
            y_coord = random.randint(0, self.length-1)
            # TODO add a check here to make sure we are only populating zero spots
            self.world[x_coord][y_coord] = level

    def print_board(self):
        print "The board currently: \n"
        for line in xrange(self.length):
            print self.world[line]
        print "\n That is the board."

    def show_board(self):
        plt.imshow(self.world)
        plt.show()

class World(object):

    def __init__(self, seed=500):
        self.plainboard = WorldGrid()
        self.plainboard.populate(n=seed)
        self.populated_board = WorldGrid
        self.creature_list = []
        for _ in xrange(100):
            self.creature_list.append(Creature())
        for _ in xrange(25):
            self.creature_list.append(Creature(level=3))

    def update_populated_board(self):
        # clear populated board
        self.populated_board = copy.deepcopy(self.plainboard)
        for creature in self.creature_list:
            self.populated_board.world[creature.x][creature.y] = creature.level

    def update_board(self):
        # let's add some more grass
        pass

    def update_creatures(self):
        for creature in self.creature_list:
            creature.update(self.plainboard, self.creature_list)

    def print_status(self):
        status, counts = np.unique(self.populated_board.world, return_counts=True)
        state = dict(zip(status, counts))
        print "There are currently {} patches of land".format(state[1])
        print "There are currently {} level 2 predators".format(state[2])
        print "There are currently {} level 3 predators".format(state[3])

    def show(self):
        self.populated_board.show_board()

def main():
    w = World()
    w.update_board()
    w.update_populated_board()
    w.print_status()
    w.show()
    for _ in xrange(3):
        w.update_creatures()
    w.update_populated_board()
    w.print_status()
    w.show()

if __name__ == "__main__":
    main()