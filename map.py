from vector2d import Vector2D
from car import Car

class Map:
    def __init__(self, id, width, height, car, walls): #multi: car->cars array
        self.id = id
        self.width = width
        self.height = height
        self.car = car
    def check_collision(self):
        for wall in self.walls:
            if pg.sprite.collide_rect(self.car, wall):
                self.car.collision(wall)