import pygame as pg
from vector2d import Vector2D
from __future__ import annotations
from car import Car


class Booster (pg.sprite.Sprite):
    def __init__(self, position: Vector2D, change: int, dt):
        pg.sprite.Sprite.__init__(self)
        self.speed_change = change
        self.position = position
        self.image = pg.image.load("./data/booster.png").convert() # make booster
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.dt = dt #refresh rate -> to use in car

    def activate(self, car: Car):
        if self.speed_change >= 0:
            car.accelerate(self.dt)

        else:
            car.decelerate(self.dt)
