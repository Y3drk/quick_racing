from __future__ import annotations

import random

import pygame as pg

from vector2d import Vector2D
from car import Car
from map import Map
from stopwatch import Stopwatch
from booster import Booster
from boosterType import BoosterType
from CSVParser import CSVParser


class NitroBar():
    def __init__(self, x, y, w, h, bg_color, color, font):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bg_color = bg_color
        self.color = color
        self.bg_rect = pg.Rect(x, y, w, h)
        self.font = font

    def draw(self, surf, val, cap):
        pg.draw.rect(surf, self.bg_color, self.bg_rect)
        rect = pg.Rect(self.x + 5, self.y + 5, int((self.w - 10) * max(val / cap, 0)), self.h - 10)
        pg.draw.rect(surf, self.color, rect)
        nitro_text = self.font.render("NITRO", 1, (0, 0, 0))
        surf.blit(nitro_text, nitro_text.get_rect(center=self.bg_rect.center))


class Engine:
    def __init__(self, refresh_rate, name, car, map):
        self.refresh = refresh_rate
        pg.init()
        self.screen = pg.display.set_mode((1480, 780))
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        self.clock = pg.time.Clock()
        self.player_name = name
        self.car = car
        self.map = map
        self.nitro_bar = NitroBar(5, 5, 250, 40, (240, 230, 140), (100, 100, 255), pg.font.SysFont('Calibri', 35))

    def spawn_booster(self, map: Map, dt):
        if random.randrange(0, 256) != 8:
            return

        place = random.randrange(0, len(map.places_for_boosters) - 1)
        x_coordinate = random.randrange(map.places_for_boosters[place][0], map.places_for_boosters[place][2])
        y_coordinate = random.randrange(map.places_for_boosters[place][1], map.places_for_boosters[place][3])

        what_booster = random.randrange(0, 6)
        new_booster_type = None
        change = None

        if what_booster == 0:
            new_booster_type = BoosterType.SPEED
            change = random.SystemRandom.uniform(-0.95, 1.00)

        elif what_booster == 1:
            new_booster_type = BoosterType.TURNING
            change = random.randrange(-3, 3)

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

    def display_laps(self, map):
        out = 'laps {lp}/6'.format(lp=map.laps_completed)
        map.font.render_to(self.screen, (1100, 40), out, pg.Color('black'))

    def start_timer(self):
        stopwatch = Stopwatch(self.screen, self.clock, Vector2D(1300, 40))
        stopwatch.restart_timer(pg.time.get_ticks())
        return stopwatch

    def run(self):
        traction = 0.15

        x, y = self.screen.get_size()

        run = True
        stopwatch = self.start_timer()

        curr_map = Map(self.map, x, y, stopwatch, self.player_name)
        map_img = pg.image.load("./data/grass.png")
        curr_map.place_objects()

        id, name, engine = CSVParser(None, None, "./data/Cars.csv").read_car_statistics(self.car)
        car = Car(id, Vector2D(50, 100), 0, 0, 10, engine, name, curr_map)

        while run:
            dt = self.clock.tick(self.refresh)
            self.screen.blit(map_img, (0, 0))

            curr_map.all_surfaces.draw(self.screen)
            curr_map.all_surfaces.update()

            curr_map.all_walls.draw(self.screen)
            curr_map.all_walls.update()

            self.spawn_booster(curr_map, dt)

            curr_map.all_boosters.draw(self.screen)
            curr_map.all_boosters.update()

            self.nitro_bar.draw(self.screen, car.nitro_dur, car.nitro_cap)

            car.move(dt)
            car.update(dt)

            self.screen.blit(car.image, (car.position.x, car.position.y))

            self.display_laps(curr_map)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            ticks = pg.time.get_ticks()
            stopwatch.display_timer(ticks)

            pg.display.flip()
