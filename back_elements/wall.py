import pygame as pg
from back_elements.vector2d import Vector2D


class Wall(pg.sprite.Sprite):
    def __init__(self, position: Vector2D, width: int, height: int, with_tires: bool, rotation):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))

        if with_tires:
            self.image = pg.image.load("data/tirewall.png").convert()
            self.image.set_colorkey((0, 0, 0))
            self.image = pg.transform.rotate(self.image, rotation)

        else:
            self.image.fill((192, 192, 192))
            self.image.set_colorkey((255, 255, 255))
            self.width = width
            self.height = height

        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.mask = pg.mask.from_surface(self.image)

        if with_tires:
            self.width = position.x - self.rect.right
            self.height = position.y - self.rect.bottom

        else:
            self.width = width
            self.height = height
    