import pygame as pg
from vector2d import Vector2D
from __future__ import annotations
from car import Car
from boosterType import BoosterType


class Booster (pg.sprite.Sprite):
    def __init__(self, position: Vector2D, change: int, image_name, type: BoosterType, dt): #change -> wartośc zmiany, jesli dotyczy zmian boolowskich to ==1
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("./data/"+image_name+".png").convert() # make booster images
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

        self.type = type
        self.int_booster_value = change
        self.duration = 3

        self.dt = dt #refresh rate -> to use in car

        self.position = position

    def activate(self, car: Car):
            if self.type == BoosterType.SPEED:
                car.speed += self.int_booster_value

            elif self.type == BoosterType.TURNING: #turning is smoother/faster or slower
                pass

            elif self.type == BoosterType.NO_COLLISIONS: #the car is "transparent"
                pass

            elif self.type == BoosterType.DECREASE_TIMER: #the time of the lap is decreased
                pass

            elif self.type == BoosterType.FREEZE:
                car.speed = 0

            else: #BoosterType.NO_TURNING -> self descriptive
                pass

            # we gotta find a way to make it last only a short amount of time -> like 3 seconds or so
            
            #we can use dt
            #we can also add "push" or something - it'd be like booster but with a single push (increase in speed in facing direction)

