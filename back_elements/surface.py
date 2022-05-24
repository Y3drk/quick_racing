from __future__ import annotations
import pygame as pg
from back_elements.vector2d import Vector2D
from enums_and_parser.surfaceType import SurfaceType


class Surface(pg.sprite.Sprite):
    def __init__(self, position: Vector2D, width: int, height: int, fraction: SurfaceType, rotation):
        pg.sprite.Sprite.__init__(self)

        if type(fraction.value[1]) == tuple:
            self.image = pg.Surface((width, height))
            self.image.fill(fraction.value[1])

        else:
            self.image = pg.image.load(fraction.value[1]).convert_alpha()
            self.image = pg.transform.rotate(self.image, rotation)

        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.width = width
        self.height = height
        self.fraction = fraction.value[0]
        self.type = fraction.name
        self.checked = False #for checkpoints mainly

        self.mask = pg.mask.from_surface(self.image)

    def adjust_fraction(self):
        return self.fraction