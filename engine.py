from __future__ import annotations
import pygame as pg
from vector2d import Vector2D
from car import Car
from map import Map
from wall import Wall
from surface import Surface
from surfaceType import SurfaceType
from stopwatch import Stopwatch
from booster import Booster
from boosterType import BoosterType
from math import sin, cos, radians


class Engine:
    def __init__(self, refresh_rate):
        self.refresh = refresh_rate
        pg.init()
        self.screen = pg.display.set_mode()
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        self.clock = pg.time.Clock()

        #move to map
        # self.all_walls = pg.sprite.Group()
        # self.all_surfaces = pg.sprite.Group()

        #it would be nice if booster stayed here
        self.all_boosters = pg.sprite.Group()

    # btw that's how we can load the map -> read all walls size and location from CSV then create
    # them and add them all to sprite group,
    # same probably could be done with ground types -> we can also handle fraction using collisions :)
    # also I think it would be beneficial if all_walls were an attribute of the map
    
    #thought exactly the same thing :) -> can be done today during labs

    def start_timer(self):
        stopwatch = Stopwatch(self.screen, self.clock, Vector2D(800, 50))
        stopwatch.restart_timer(pg.time.get_ticks())
        return stopwatch

    def run(self):
        #temporarily for boosters
        # booster1 = Booster(Vector2D(700, 700), 30, "dt",BoosterType.SPEED, self.clock.tick(self.refresh))
        # self.all_boosters.add(booster1)

        traction = 0.15

        # car_img = pg.image.load("./data/car.png") #done temporarily inside the car class

        x, y = self.screen.get_size()

        curr_map = Map(0, x, y)
        map_img = pg.image.load("./data/grass.png")
        curr_map.place_objects()

        car = Car(0, Vector2D(10, 10), 0, 0, 10, 50, curr_map)

        run = True
        stopwatch = self.start_timer()

        while run:
            dt = self.clock.tick(self.refresh)
            self.screen.blit(map_img, (0, 0))

            curr_map.all_surfaces.draw(self.screen)
            curr_map.all_surfaces.update()

            #self.screen.blit(car.image, (car.position.x, car.position.y))
            #self.all_cars.draw(self.screen)
            #added

            curr_map.all_walls.draw(self.screen)
            curr_map.all_walls.update()

            car.move(dt) # maybe car also should be coded as a sprite???
            car.update(dt)

            self.screen.blit(car.image, (car.position.x, car.position.y))

            #pg.draw.rect(self.screen, (0,0,0), car, 3)



            #print(traction) no we have to include different surfaces in the movement of the car

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            ticks = pg.time.get_ticks()
            stopwatch.display_timer(ticks)


            pg.display.flip()