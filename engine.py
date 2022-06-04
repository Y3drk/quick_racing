from __future__ import annotations

import random

import pygame as pg

from back_elements.vector2d import Vector2D
from back_elements.car import Car
from back_elements.map import Map
from back_elements.stopwatch import Stopwatch
from back_elements.booster import Booster
from enums_and_parser.boosterType import BoosterType
from enums_and_parser.CSVParser import CSVParser


class Results:
    def __init__(self, x, y, w, h, bg_color, color, font, button_font):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bg_color = bg_color
        self.color = color
        self.font = font
        self.button_font = button_font
        self.bg_rect = pg.Rect(x, y, w, h)
        self.finished_rect = pg.Rect(x + 10, y + 10, w - 20, 40)
        self.return_to_menu_rect = pg.Rect(x + 10, y + h - 30, w // 2 - 20, 25)
        self.restart_rect = pg.Rect(x + w // 2 + 10, y + h - 30, w // 2 - 20, 25)
        self.return_text_rect = pg.Rect(x + 10, y + h - 30, w // 2 - 20, 25)
        self.restart_text_rect = pg.Rect(x + w // 2 + 10, y + h - 30, w // 2 - 20, 25)

    def draw(self, surf, times, pressed):
        pg.draw.rect(surf, self.bg_color, self.bg_rect)
        pg.draw.rect(surf, self.color, self.finished_rect)
        finished = self.font.render("FINISHED!", 1, (0, 0, 0))
        surf.blit(finished, finished.get_rect(center=self.finished_rect.center))
        results = [pg.Rect(self.x + 10, self.y + 60 + 50 * i, self.w - 20, 40) for i in range(6)]
        for i in range(6):
            t = self.font.render(times[i], 1, (0, 0, 0))
            surf.blit(t, t.get_rect(center=results[i].center))

        return_button = pg.draw.rect(surf, self.color, self.return_to_menu_rect)
        restart_button = pg.draw.rect(surf, self.color, self.restart_rect)
        return_text = self.button_font.render("To menu", 1, (0, 0, 0))
        restart_text = self.button_font.render("Restart", 1, (0, 0, 0))
        surf.blit(return_text, return_text.get_rect(center=self.return_text_rect.center))
        surf.blit(restart_text, restart_text.get_rect(center=self.restart_text_rect.center))
        if return_button.collidepoint(pg.mouse.get_pos()):
            return_color = (240, 230, 140)
            if pressed:
                return 0
        else:
            return_color = (100, 200, 255)

        if restart_button.collidepoint(pg.mouse.get_pos()):
            restart_color = (240, 230, 140)
            if pressed:
                return 1
        else:
            restart_color = (100, 200, 255)

        pg.draw.rect(return_text, return_color, [self.x + 10, self.y + self.h - 30, self.w // 2 - 20, 25])
        pg.draw.rect(restart_text, restart_color,
                     [self.x + self.w // 2 + 10, self.y + self.h - 30, self.w // 2 - 20, 25])
        return 2


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
        self.results_popup = Results(1480 // 2 - 300 // 2, 780 // 2 - 400 // 2, 300, 400, (240, 230, 140),
                                     (100, 100, 255), pg.font.SysFont('Calibri', 35), pg.font.SysFont('Calibri', 25))

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
            change = random.uniform(-0.95, .5)

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

            self.nitro_bar.draw(self.screen, car.nitro_duration, car.nitro_capacity)

            car.move(dt)
            car.update(dt)

            self.screen.blit(car.image, (car.position.x, car.position.y))

            self.display_laps(curr_map)

            pressed = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pressed = True

            ticks = pg.time.get_ticks()
            stopwatch.display_timer(ticks)

            if curr_map.won == 1:
                r = self.results_popup.draw(self.screen, curr_map.times, pressed)
                if r == 0:
                    run = False
                elif r == 1:
                    self.run()

            pg.display.flip()
        pg.display.set_mode((1080, 720))
