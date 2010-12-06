#!/usr/bin/env python


import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import math

class Block(object):
    def __init__(self, space, pos_x, pos_y, width, height):
        body = pymunk.Body(pymunk.inf, pymunk.inf)
        body.position = (pos_x, pos_y)
        corners = [(0,0), (width,0), (width, height), (0, height)]
        contour = pymunk.Poly(body, corners, offset=(-width/2, -height/2))
        space.add(contour, body)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.corners = corners
        self.width = width
        self.height = height

    def draw(self, screen):
        rect = pygame.Rect(self.pos_x - self.width,
                           self.pos_y - self.height,
                           self.width, self.height)
        pygame.draw.rect(screen, THECOLORS['red'], rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("blocks.")
    clock = pygame.time.Clock()
    running = True
    
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    blocks = [Block(space, 200, 200, 50, 50)]
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        screen.fill(THECOLORS["white"])
        
        #space.step(1/50.0)

        for block in blocks:
            block.draw(screen)
        
        pygame.display.flip()
        clock.tick(50)
        
if __name__ == '__main__':
    sys.exit(main())
