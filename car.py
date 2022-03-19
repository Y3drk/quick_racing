import pygame as pg
from vector2d import Vector2D
from math import sin, cos, radians


class Car(pg.sprite.Sprite): #https://asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html
    def __init__(self, id, position, speed, direction, rotation, engine):
        #super().__init__()
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("./data/car.png").convert()
        #self.image.fill((0, 0, 0))
        self.image.set_colorkey((255, 255, 255))  # this will make the img ignore all the white pixels
        self.rect = self.image.get_rect()
        self.rect.center = (position.x, position.y)


        self.id = id
        self.position = position
        self.speed = speed
        self.direction = direction
        self.rotation = rotation
        self.engine = engine

    def update(self, dt):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_UP]:
            self.accelerate(dt)
        if pressed[pg.K_DOWN]:
            self.decelerate(dt)
        if pressed[pg.K_LEFT]:
            self.rotate_left(dt)
        if pressed[pg.K_RIGHT]:
            self.rotate_right(dt)

    def move(self, dt):
        if self.speed > 0:
            self.speed -= self.speed * (0.03 + self.speed * 0.1) #v drogi i v*v powietrza
        elif self.speed < 0:
            self.speed += self.speed * (0.03 + self.speed * 0.1) #v drogi i v*v powietrza
        self.position.add(self.speed*cos(radians(self.direction)), self.speed*sin(radians(self.direction)))
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        if self.rect.left > 400: #for now hardcoded
            self.rect.right = 0


    def collision(self, wall):
        self.direction += 180 - abs(self.direction - wall.get_facing)

    def rotate_left(self, dt):
        if self.speed != 0:
            self.direction -= 2 * self.rotation/(dt * self.speed)
            if self.direction < 0:
                self.direction += 360

    def rotate_right(self, dt):
        if self.speed != 0:
            self.direction += 2 * self.rotation/(dt * self.speed)
            if self.direction > 360:
                self.direction -= 360

    def accelerate(self, dt):
        self.speed += self.engine/dt

    def decelerate(self, dt):
        self.speed -= self.engine/(2*dt)