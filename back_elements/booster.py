from __future__ import annotations
import pygame as pg
from back_elements.vector2d import Vector2D
from back_elements.car import Car
from enums_and_parser.boosterType import BoosterType
from back_elements.stopwatch import Stopwatch


class Booster(pg.sprite.Sprite):
    def __init__(self, position: Vector2D, change: int, type: BoosterType, dt):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(
            "./data/quick_racing_booster_" + type.value[1] + ".png").convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

        self.type = type
        self.initial_booster_value = change
        self.duration = 80

        self.dt = dt
        self.position = position
        self.mask = pg.mask.from_surface(self.image)

    def activate(self, car: Car, stopwatch: Stopwatch):
        if self.type == BoosterType.SPEED:
            car.boosters["speed"] = [self.initial_booster_value, pg.time.get_ticks() * self.duration]

        elif self.type == BoosterType.TURNING:
            car.boosters["turning"] = [self.initial_booster_value, pg.time.get_ticks() * 0.5 * self.duration]

        elif self.type == BoosterType.NO_COLLISIONS:
            car.boosters["transparent"] = [True, pg.time.get_ticks() * self.duration]

        elif self.type == BoosterType.DECREASE_TIMER:
            stopwatch.decrease_timer(4000)

        elif self.type == BoosterType.FREEZE:
            car.boosters["freeze"] = [True, pg.time.get_ticks() * self.duration]

        else:
            car.boosters["noTurning"] = [True, pg.time.get_ticks() * 0.5 * self.duration]
