import pygame as pg
from vector2d import Vector2D
from math import sqrt, acos


class Wall(pg.sprite.Sprite):
    def __init__(self, position: Vector2D, width: int, height: int, with_tires: bool, rotation):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))

        if with_tires:
            self.image = pg.image.load("./data/tirewall.png").convert()
            self.image.set_colorkey((0, 0, 0))
            self.image = pg.transform.rotate(self.image, rotation)

        else:
            self.image.fill((192, 192, 192))
            self.image.set_colorkey((255, 255, 255)) #this will make the img ignore all the white pixels
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

    # def get_facing(self):
    #     x_diff = self.lower_left_corner.x - self.upper_right_corner.x
    #     y_diff = self.lower_left_corner.y - self.upper_right_corner
    #     r = sqrt(x_diff*x_diff + y_diff*y_diff)
    #     angle = acos(x_diff / r) + 90
    #     if angle < 0:
    #         angle += 360
    #     elif angle >= 360:
    #         angle -= 360
    #
    #     return angle
    