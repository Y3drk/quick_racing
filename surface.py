import pygame as pg
from vector2d import Vector2D
from __future__ import annotations
from surfaceType import SurfaceType


class Surface(pg.sprite.Sprite):
    def __init__(self, position: Vector2D, width: int, height: int, fraction: SurfaceType):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill((255, 255, 255)) #for now it's all white but we should figure out how to colour it differently
        self.image.set_colorkey((0, 0, 0)) #this will make the img ignore all the white pixels
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.width = width
        self.height = height
        self.fraction = fraction.value

        if fraction == SurfaceType.ASPHALT:
            pass

