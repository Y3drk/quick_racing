import pygame as pg
from vector2d import Vector2D
from math import sqrt, acos

class Wall(pg.sprite.Sprite):
    def __init__(self, lower_left_corner: Vector2D, upper_right_corner: Vector2D):
        super().__init__()
        
        self.lower_left_corner = lower_left_corner
        self.upper_right_corner = upper_right_corner  #for now it's a rectangle
        self.height = (upper_right_corner.subtract_vector(lower_left_corner)).y
        self.length = (upper_right_corner.subtract_vector(lower_left_corner)).x
    def get_facing(self):
        x_diff = self.lower_left_corner.x - self.upper_right_corner.x
        y_diff = self.lower_left_corner.y - self.upper_right_corner
        r = sqrt(x_diff*x_diff + y_diff*y_diff)
        angle = acos( x_diff / r ) + 90
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle -= 360
        return angle