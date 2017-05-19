import copy
import random
import time

import numpy as np
import pygame as pg


class Creature(object):
    # We are moving the Creature class out of the world class and keeping track of it separate
    def __init__(self, x, y, level, hunger, world, size, color, thickness, eats=1, move_heuristic=None):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.thickness = thickness

        self.level = level
        self.eats = eats
        self.hunger = hunger
        self.vegetarian = self.eats == 1

        # a reference to the world object
        self.world = world
        self.move_heuristic = move_heuristic

    def display(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)

    def move(self):
        # TODO currently moving is random, but later we'll add behavior and heuristics like searching or avoidance
        if self.move_heuristic is None:
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
        else:
            (dx, dy) = self.move_heuristic(self)

        self.x = (self.x + dx) % self.world_dimensions[0]
        self.y = (self.y + dy) % self.world_dimensions[1]


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

    def __init__(self, length, width):
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



class World(object):

    def __init__(self, x, y, seed=500):
        self.x = x
        self.y = y
        self.board = self.board = np.zeros((x, y), dtype=np.int)
        for i in xrange(seed):
            x_coord = random.randint(0, x - 1)
            y_coord = random.randint(0, y - 1)
            while self.board[x_coord][y_coord] == 1:  # check to make sure we only add to 'empty' squares
                x_coord = random.randint(0, x - 1)
                y_coord = random.randint(0, y - 1)
            self.board[x_coord][y_coord] = 1

    def display(self, screen):
        for x in xrange(self.x):
            for y in xrange(self.y):
                if self.board[x][y] == 1:
                    pg.draw.circle(screen, (0,255,0), (x,y), 5, 5)

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
    # initialize our world
    w = World(800, 600)
    # w.update_board()
    # w.update_populated_board()
    creature_list = []
    for i in xrange(100):
        # let's create some herbivores
        c = Creature(random.randint(0,800), random.randint(0,600), 2, 10, w, 5, (0, 0, 255), 2, 1)
        creature_list.append(c)

    # initializing our display
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Predator Prey Simulation")
    screen.fill((255, 255, 255))
    w.display(screen)
    for c in creature_list:
        c.display(screen)
    pg.display.flip()

    for i in xrange(20):
        # w.update_creatures()
        # w.update_populated_board()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
