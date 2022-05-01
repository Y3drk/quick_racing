from __future__ import annotations

import asyncio
import random

import pygame as pg

import boosterType
from vector2d import Vector2D
from car import Car
from map import Map
from stopwatch import Stopwatch
from booster import Booster
from boosterType import BoosterType
from math import sin, cos, radians


class Engine:
    def __init__(self, refresh_rate):
        self.refresh = refresh_rate
        pg.init()
        self.screen = pg.display.set_mode((1480,780))
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        self.clock = pg.time.Clock()

    def spawn_booster(self, map: Map, dt):

        if random.randrange(0, 256) != 8:
            return

        place = random.randrange(0, len(map.places_for_boosters)-1)
        x_coordinate = random.randrange(map.places_for_boosters[place][0], map.places_for_boosters[place][2])
        y_coordinate = random.randrange(map.places_for_boosters[place][1], map.places_for_boosters[place][3])


        what_booster = random.randrange(0,5)
        new_booster_type = None
        change = None

        #temp
        ctrl = random.randrange(0, 2)
        if ctrl == 0:
            what_booster = 3
        else:
            what_booster = 2
        #temp

        if what_booster == 0:
            new_booster_type = BoosterType.SPEED
            change = random.randrange(-100, 100)

        elif what_booster == 1:
            new_booster_type = BoosterType.TURNING
            change = random.randrange(-3 , 3)

        elif what_booster == 2:
            new_booster_type = BoosterType.NO_COLLISIONS
            change = 1

        elif what_booster == 3:
            new_booster_type = BoosterType.DECREASE_TIMER
            change = 1

        elif what_booster == 4:
            new_booster_type = BoosterType.NO_TURNING
            change = 1

        elif what_booster == 5:
            new_booster_type = BoosterType.FREEZE
            change = 1

        map.all_boosters.add(Booster(Vector2D(x_coordinate, y_coordinate), change, new_booster_type, dt))
        #print("Booster spawned!\n")


    def start_timer(self):
        stopwatch = Stopwatch(self.screen, self.clock, Vector2D(1300, 40))
        stopwatch.restart_timer(pg.time.get_ticks())
        return stopwatch

    def run(self):
        #temporarily for boosters
        # booster1 = Booster(Vector2D(700, 700), 30, "dt",BoosterType.SPEED, self.clock.tick(self.refresh))
        # self.all_boosters.add(booster1)

        traction = 0.15

        # car_img = pg.image.load("./data/car.png") #done temporarily inside the car class

        x, y = self.screen.get_size()

        run = True
        stopwatch = self.start_timer()

        curr_map = Map(0, x, y, stopwatch)
        map_img = pg.image.load("./data/grass.png")
        curr_map.place_objects()

        car = Car(0, Vector2D(50, 100), 0, 0, 10, 50, curr_map)

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

            self.spawn_booster(curr_map, dt)

            curr_map.all_boosters.draw(self.screen)
            curr_map.all_boosters.update()

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