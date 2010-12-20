import json
import random
import pygame
import pymunk
from pygame.color import *
from pygame.locals import *

def to_pygame(p, screen):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+screen.get_height())

class World(object):
    def __init__(self):
        self.objects = []
        pymunk.init_pymunk()
        space = pymunk.Space()
        space.gravity = (0.0, -900.0)
        self.space = space

    def get_state(self):
        for shape in self.objects:
            yield shape.get_state()

    def save_level(self, filename):
        with open(filename, "w") as f:
            json.dump(list(self.get_state()), f)

    def load_level(self, filename):
        with open(filename) as f:
            level = json.load(f)
        self.objects.extend([Block(self.space, *block)
                             for block in level['blocks']])

    def append(self, ob):
        self.objects.append(ob)

    def draw(self, screen):
        for shape in self.objects:
            shape.draw(screen)

class Block(object):
    #def __init__(self, space, pos_x, pos_y, points, static=False):
    #    density = .0007
    #    if static:
    #        body = pymunk.Body(pymunk.inf, pymunk.inf)
    #    else:
    #        body = pymunk.Body(density * width * height,
    #                           1000 * density * width * height)
    #    body.position = (pos_x, pos_y)
    #    self.body = body
    #    corners = self.body.world_to_local(points)
    #    contour = pymunk.Poly(body, corners, offset=(0, 0))
    #    space.add(contour)
    #    if not static:
    #        space.add(body)
    #    self.contour = contour
    #    self.contour.friction = .5
    #    self.contour.elasticity = 0.5
    #    self.color = random.choice(THECOLORS.values())
    #    self.static = static

    def __init__(self, space, pos_x, pos_y, width, height, static=False):
        density = .0007
        if static:
            body = pymunk.Body(pymunk.inf, pymunk.inf)
        else:
            body = pymunk.Body(density * width * height,
                               1000 * density * width * height)
        body.position = (pos_x, pos_y)
        corners = [(0,0), (width,0), (width, height), (0, height)]
        contour = pymunk.Poly(body, corners, offset=(-width/2, -height/2))
        space.add(contour)
        if not static:
            space.add(body)
        self.contour = contour
        self.contour.friction = .5
        self.contour.elasticity = 0.5
        self.body = body
        self.static = static
        self.color = random.choice(THECOLORS.values())


    def draw(self, screen):
        pointlist = [to_pygame(point, screen)
                     for point in self.contour.get_points()]
        pygame.draw.polygon(screen, self.color, pointlist)

    def get_state(self):
        return {
            "type":"blocks",
            "pos_x":self.body.position[0],
            "pos_y":self.body.position[1],
            "points":[tuple(p) for p in self.contour.get_points()],
            "static":self.static}

class Ball(object):
    def __init__(self, space, pos_x, pos_y, radius):
        density = .0007
        mass = density * (3.14 * radius ** 2)
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        body = pymunk.Body(mass, inertia)
        body.position = (pos_x, pos_y)
        circle = pymunk.Circle(body, radius, (0, 0))
        circle.elasticity = 0.9
        space.add(body, circle)
        self.circle = circle
        self.body = body
        self.color = random.choice(THECOLORS.values())

    def draw(self, screen):
        position = to_pygame(self.body.position, screen)
        pygame.draw.circle(screen, self.color, position, self.circle.radius)

    #def get_state(self):
    #    return {
    #        "type":"ball",
    #        "points":self.contour.get_points(),
    #        "static":self.static}

    def apply_impulse(self, x, y):
        self.body.apply_impulse(pymunk.Vec2d(x, y))
