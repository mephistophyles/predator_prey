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

        self.world = world
        self.level = level
        self.eats = eats
        self.hunger = hunger
        self.vegetarian = self.eats == 1

        # beauty of python, we can pass functions as function parameters
        self.move_heuristic = move_heuristic

    def display(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)

    def move(self, world):
        if self.move_heuristic is None:
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
        else:
            (dx, dy) = self.move_heuristic(self, world)

        # TODO fix this, so they don't seem to pop over the edge and appear on the other side
        self.x = (self.x + dx) % self.world.x
        self.y = (self.y + dy) % self.world.y

    def update(self, world):
        # if self.hunger <= 0:
            # he dead
            # return False
        self.hunger -= 1
        # for now we will add all the moving and eating in the move function
        self.move(world)
        # TODO add some form of procreation


#TODO add different heuristics for the movement of creatures


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

    def update(self):
        # TODO clean up this procreation randomness
        for x in xrange(self.x):
            for y in xrange(self.y):
                if self.board[x][y] == 1:
                    fill = random.random()
                    # print fill
                    if fill < 0.01 and x < 790 and y < 590:
                        self.board[x + 9][y] == 1
                        self.board[x][y + 9] == 1
                        self.board[x + 9][y + 9] = 1


def main():
    # initialize our world
    w = World(800, 600, 1000)
    creature_list = []
    # let's create some herbivores
    for _ in xrange(500):
        c = Creature(random.randint(0, 800), random.randint(0, 600), 2, 10, w, 5, (0, 0, 255), 2, 1)
        creature_list.append(c)
    # let's create some carnivores
    for _ in xrange(100):
        c = Creature(random.randint(0, 800), random.randint(0, 600), 3, 25, w, 4, (255, 0, 0), 4, 2)
        creature_list.append(c)

    # initializing our display
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Predator Prey Simulation")
    background_color = (255, 255, 255)
    screen.fill(background_color)
    w.display(screen)
    for c in creature_list:
        c.display(screen)
    pg.display.flip()

    # main eventloop TODO: later we will check for input and run indefinitely or till we have an extinction event
    for i in xrange(100):
        print "Current plants {}".format(np.sum(w.board))
        screen.fill(background_color)
        w.display(screen)
        w.update()
        for c in creature_list:
            c.update(w)
            c.display(screen)
        pg.display.flip()

if __name__ == "__main__":
    main()
