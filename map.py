from vector2d import Vector2D
from car import Car

class Map:
    def __init__(self, id, width, height, car): #multi: car->cars array
        self.id = id
        self.width = width
        self.height = height
        self.car = car
        