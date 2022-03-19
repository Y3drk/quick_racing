import pygame as pg
from vector2d import Vector2D
from math import sqrt, acos


class Wall(pg.sprite.Sprite):
    def __init__(self, position: Vector2D, width: int, height: int):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((255, 255, 255)) #this will make the img ignore all the white pixels
        self.rect = self.image.get_rect()
        self.rect.center = (position.x, position.y)

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
    