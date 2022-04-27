from __future__ import annotations 
import pygame as pg
from vector2d import Vector2D
from car import Car


class Map:
    def __init__(self, id, width, height, car, walls, surfaces): #surfaces
        self.id = id
        self.width = width
        self.height = height
        self.car = car
        self.walls = walls
        self.surfaces = surfaces
        self.name = "Map"

    def check_collision(self):
        for wall in self.walls:
            if pg.sprite.collide_rect(self.car, wall):
                self.car.collision(wall)
    
    def collision_test(self):
        collisions = []
        c = self.car
        for wall in self.walls:
            if pg.c.collide_rect(wall):
                collisions.append(wall)
        for collision in collisions:
            self.car.collide()