from vector2d import Vector2D
from math import sin, cos, radians

class Car: #https://asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html
    def __init__(self, id, position, speed, direction, rotation):
        self.id = id
        self.position = position
        self.speed = speed
        self.direction = direction
        self.rotation = rotation
    def rotate_left(self, dt):
        self.direction -= self.rotation
        if self.direction < 0:
            self.direction += 360
    def rotate_right(self, dt):
        self.direction += self.rotation
        if self.direction > 360:
            self.direction -= 360
    def accelerate(self, dt):
        self.position.add(self.speed*cos(radians(self.direction)), self.speed*sin(radians(self.direction)))
    def decelerate(self, dt):
        self.position.subtract( self.speed*cos(radians(self.direction)), self.speed*sin(radians(self.direction)))
    