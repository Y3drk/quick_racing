from __future__ import annotations
import pygame as pg

from enums_and_parser.CSVParser import CSVParser

from math import sin, cos, radians


class Map:
    def __init__(self, in_game_id, width, height, stopwatch, player_name):
        self.id = in_game_id
        self.width = width
        self.height = height
        self.all_walls = pg.sprite.Group()
        self.all_surfaces = pg.sprite.Group()
        self.all_boosters = pg.sprite.Group()
        self.places_for_boosters = []
        self.name = "map{}".format(in_game_id + 1)
        self.stopwatch = stopwatch
        self.player_name = player_name
        self.checkpoints = []
        self.placement = 0

        self.font = pg.freetype.SysFont(None, 34)
        self.font.origin = True
        self.laps_completed = 0

        self.times = []
        self.won = 0

        self.prev_car_rect = (0, 0)

    def place_objects(self):
        parser = CSVParser("./data/" + self.name + ".csv", "./data/Leaderboard.csv", None)
        parser.draw_map(self)

    def increment_laps(self):
        self.laps_completed += 1

    def handle_collision_with_walls(self, car):
        if car.boosters["transparent"][0]:
            return None, False

        collisions = pg.sprite.spritecollide(car, self.all_walls, False, pg.sprite.collide_mask)
        if collisions:
            for col in collisions:
                if abs(self.prev_car_rect[0] - car.rect.width) < 4 and \
                        abs(self.prev_car_rect[1] - car.rect.height) < 4 and car.collision_facilitator[0]:
                    return "side", True
                else:
                    self.prev_car_rect = (car.rect.width, car.rect.height)
                    return "other", True

        return None, False

    def handle_collision_with_surfaces(self, car):
        slides = pg.sprite.spritecollide(car, self.all_surfaces, False, pg.sprite.collide_mask)
        if slides:
            for slide in slides:
                if slide.type == "FINISHLINE":
                    if False not in self.checkpoints:
                        if self.won == 0:
                            self.times.append(self.stopwatch.get_time(pg.time.get_ticks()))

                            with open("data/Records.csv", "a") as f:
                                f.write("\n{},{},{},{}".format(car.name, self.name,
                                                               self.stopwatch.get_time(pg.time.get_ticks()),
                                                               self.player_name))
                            self.stopwatch.restart_timer(pg.time.get_ticks())
                            self.placement = 0

                            for i in range(0, len(self.checkpoints)):
                                self.checkpoints[i] = False

                            for slide in self.all_surfaces:
                                slide.checked = False

                            self.increment_laps()
                        if self.laps_completed == 6:
                            self.won = 1
                            self.times = [
                                "{minutes:02d}.{seconds:02d}.{millis}".format(minutes=int(self.times[i] / 60000 % 24),
                                                                              millis=self.times[i] % 1000,
                                                                              seconds=int(self.times[i] / 1000 % 60))
                                for i in range(6)]

                if slide.type == "CHECKPOINT":
                    if self.placement <= len(self.checkpoints) - 1 and \
                            self.checkpoints[self.placement] == False and slide.checked == False:

                        self.checkpoints[self.placement] = True
                        self.placement += 1
                        slide.checked = True

                if slide.rect.x == car.rect.x + car.speed * cos(radians(car.direction)) \
                        and slide.rect.y == car.rect.y + car.speed * sin(radians(car.direction)):
                    return slide.adjust_fraction()

    def handle_collision_with_boosters(self, car):
        pick_ups = pg.sprite.spritecollide(car, self.all_boosters, True, pg.sprite.collide_mask)
        if pick_ups:
            for boost in pick_ups:
                boost.activate(car, self.stopwatch)

    def handle_boosters(self, car):
        for t in car.boosters.values():
            t[1] -= pg.time.get_ticks()

            if t[1] <= 0:
                if t[0]:
                    t[0] = False
                else:
                    t[0] = 0

                t[1] = 0
