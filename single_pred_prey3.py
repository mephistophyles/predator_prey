# Building upon the previous file, we have a state that changes on iterations, now let's make a continuous
# simulation out of it that also shows the current stats
# We also want to add some state output and saving of data at each timestep for later processing.

# TODO consider creating a custom colormap to keep colors consistent for various Eco_depth levels and let
# the colors make more sense
# TODO also maybe create a runner that performs a number of simulations with a given set of parameters
# and then compares that to an adapted version of Lotka-Volterra equations? See how realistic this model is

import copy
import random
import time

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

WORLDLENGTH = 100  # y
WORLDWIDTH = 100  # x
ECOLOGICAL_DEPTH = 3  # the amount of levels of pred-prey, TODO maybe add an upper limit?


class Creature(object):

    def __init__(self, length=WORLDLENGTH, width=WORLDWIDTH, level=2, hunger=5, eats=1, vegetarian=True):
        self.x = random.randint(0, width-1)
        self.y = random.randint(0, length-1)
        self.level = level
        self.eats = eats
        self.hunger = hunger
        self.vegetarian = vegetarian

    def move(self):
        # TODO currently moving is random, but later we'll add behavior and heuristics like searching or avoidance
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)
        self.x = (self.x + dx) % WORLDWIDTH
        self.y = (self.y + dy) % WORLDLENGTH

    def update(self, world):
        self.move()
        self.hunger -= 1
        # TODO add some form of procreation
        if self.vegetarian:
            if world.plainboard.board[self.x][self.y] == 1:
                self.hunger += 5
                world.plainboard.board[self.x][self.y] = 0
                world.status[1] -= 1
        else:
            for creature in world.creature_list:
                # predators can 'leap' to adjacent squares
                if abs(creature.x - self.x) < 2 and abs(creature.y - self.y) < 2 and creature.level == self.eats:
                    self.hunger += 5
                    world.creature_list.remove(creature)
                    world.status[creature.level] -= 1
        if self.hunger <= 0:
            world.creature_list.remove(self)
            world.status[self.level] -= 1


class WorldGrid(object):

    def __init__(self, length=WORLDLENGTH, width=WORLDWIDTH):
        self.board = np.zeros((length, width), dtype=np.int)
        self.length = length
        self.width = width

    def populate(self, n, level=1):
        for _ in xrange(n):
            x_coord = random.randint(0, self.width-1)
            y_coord = random.randint(0, self.length-1)
            while self.board[x_coord][y_coord] == level:  # check to make sure we only add to 'empty' squares
                x_coord = random.randint(0, self.width - 1)
                y_coord = random.randint(0, self.length - 1)
            self.board[x_coord][y_coord] = level


    def print_board(self):
        print "The board currently: \n"
        for line in xrange(self.length):
            print self.board[line]
        print "\n That is the board."

    def update(self):
        # TODO allow for the growing of plants to 4-adjacent tiles
        pass

    def show_board(self):
        return plt.imshow(self.board)


class World(object):

    def __init__(self, seed=500, creature_level=ECOLOGICAL_DEPTH):
        self.plainboard = WorldGrid()
        self.plainboard.populate(n=seed)
        self.populated_board = WorldGrid()
        self.creature_list = []
        self.status = {}
        # TODO make this whole creature status and creation process more elegant
        for i in range(1, creature_level):
            self.status[i] = 0
        for _ in xrange(100):
            self.creature_list.append(Creature())
        for _ in xrange(25):
            self.creature_list.append(Creature(level=3))
        for creature in self.creature_list:
            if creature.level not in self.status.keys():
                self.status[creature.level] = 1
            else:
                self.status[creature.level] += 1
        self.status[1] = seed

    def update_populated_board(self):
        # clear populated board
        self.populated_board = copy.deepcopy(self.plainboard)
        for creature in self.creature_list:
            self.populated_board.board[creature.x][creature.y] = creature.level

    def update_board(self):
        # let's add some more grass
        self.plainboard.update()

    def update_creatures(self):
        for creature in self.creature_list:
            creature.update(self)

    def get_status(self):
        output = ""
        for level in self.status.keys():
            if level == 1:
                output += "\tLand: {}\n".format(self.status[level])
            else:
                output += "\tPredators lvl {}: {}\n".format(level, self.status[level])
        return output

    def show(self):
        self.populated_board.show_board()


def main():
    w = World()
    w.update_board()
    w.update_populated_board()
    fig, ax = plt.subplots(1,1, figsize=(9,9))
    savefile = "c://Users//Philip//PycharmProjects//test_project//test.txt"
    f = open(savefile, mode='w')
    plt.ion()
    # plt.annotate(w.status(), xy=(0,0), xytext=(0,0), fontsize=10)
    # TODO factor out the animation into its own function, perhaps using Tk
    for i in xrange(20):
        w.update_creatures()
        w.update_populated_board()
        ax.imshow(w.populated_board.board, clim=(0, ECOLOGICAL_DEPTH))
        an = plt.annotate(w.get_status(), xy=(0,0), xytext=(0,0), fontsize=10)
        f.write("At timestep {}\n".format(i))
        f.write(w.get_status())
        plt.pause(0.1)
        # TODO get the status to show properly, instead of overwriting.
        del(an)
    plt.close()
    f.close()

if __name__ == "__main__":
    main()
