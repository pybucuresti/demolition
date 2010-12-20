#!/usr/bin/env python
import sys
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk

from engine import World, Ball, Block

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("blocks.")
    clock = pygame.time.Clock()
    world = World()
    world.load_level(sys.argv[1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                world.save_level(sys.argv[2])
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    mpos = mpos[0], screen.get_height() - mpos[1]
                    pygame.mouse.get_rel()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    ball = Ball(world.space, *mpos, radius=20)
                    rel = pygame.mouse.get_rel()
                    rel = rel[0] * 2, -rel[1] * 2
                    world.append(ball)
                    ball.apply_impulse(*rel)
            elif event.type == KEYDOWN and event.key == 115:
                world.space.step(1/200.0)
                print list(world.get_state())

        screen.fill(THECOLORS["white"])

        world.draw(screen)

        pygame.display.flip()
        clock.tick(200)

if __name__ == '__main__':
    sys.exit(main())
