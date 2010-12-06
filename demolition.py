#!/usr/bin/env python


import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import math
import json
def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

class Block(object):
    def __init__(self, space, pos_x, pos_y, width, height, static=False):
        density = .0007
        if static:
            body = pymunk.Body(pymunk.inf, pymunk.inf)
        else:
            body = pymunk.Body(density * width * height, 1000 * density * width * height)
        body.position = (pos_x, pos_y)
        corners = [(0,0), (width,0), (width, height), (0, height)]
        contour = pymunk.Poly(body, corners, offset=(-width/2, -height/2))
        space.add(contour)
        if not static:
            space.add(body)
        self.contour = contour
        self.contour.friction = .5
      
    def draw(self, screen):
        pointlist = [to_pygame(point) for point in self.contour.get_points()]
        pygame.draw.polygon(screen, THECOLORS['red'], pointlist)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("blocks.")
    clock = pygame.time.Clock()
    running = True
    
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    with open(sys.argv[1]) as f:
        world = json.load(f)

    blocks = [Block(space, *block) for block in world['blocks']] 
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        screen.fill(THECOLORS["white"])
        
        space.step(1/50.0)

        for block in blocks:
            block.draw(screen)
        
        pygame.display.flip()
        clock.tick(50)
        
if __name__ == '__main__':
    sys.exit(main())
