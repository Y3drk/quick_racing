from __future__ import annotations 
import pygame as pg

from CSVParser import CSVParser
from surfaceType import SurfaceType
from surface import Surface

from math import sin, cos, radians


class Map:
    def __init__(self, id, width, height, stopwatch):
        self.id = id
        self.width = width
        self.height = height
        self.all_walls = pg.sprite.Group()
        self.all_surfaces = pg.sprite.Group()
        self.all_boosters = pg.sprite.Group()
        self.places_for_boosters = []
        self.name = "Map"
        self.stopwatch = stopwatch

    def place_objects(self):
        parser = CSVParser("./data/map1.csv", "../data/Leaderboard.csv")

        parser.draw_map(self)

        #print(self.places_for_boosters)

        # surface1 = Surface(Vector2D(100, 100), 1500, 110, SurfaceType.ASPHALT)
        # self.all_surfaces.add(surface1)


        # wall1 = Wall(Vector2D(250, 300), 60, 60, False)
        # self.all_walls.add(wall1) # beginning of sprites
        # wall2 = Wall(Vector2D(20, 150), 60, 20, True)
        # self.all_walls.add(wall2)  # beginning of sprites
        #
        # surface1 = Surface(Vector2D(150, 20), 100, 50, SurfaceType.ASPHALT)
        # self.all_surfaces.add(surface1)
        # surface2 = Surface(Vector2D(400, 200), 100, 80, SurfaceType.ICE)
        # self.all_surfaces.add(surface2)
        #
        # test1 = Surface(Vector2D(wall1.rect.x, wall1.rect.y), 10, 10, SurfaceType.ICE)
        # self.all_surfaces.add(test1)

    # @staticmethod
    # def new_collision_place(x, y, wall: Wall, car):
    #     options = []
    #
    #     distance_right_wall = abs(x - wall.rect.right)
    #     options.append((distance_right_wall, "distance_right_wall"))
    #
    #     distance_left_wall = abs(x - wall.rect.left)
    #     options.append((distance_left_wall, "distance_left_wall"))
    #
    #     distance_bottom_wall = abs(y - wall.rect.bottom)
    #     options.append((distance_bottom_wall, "distance_bottom_wall"))
    #
    #     distance_top_wall = abs(y - wall.rect.top)
    #     options.append((distance_top_wall, "distance_top_wall"))
    #
    #     best = (float('inf'), None)
    #     for dist in options:
    #         if best[0] > dist[0]:
    #             best = dist
    #
    #     # print(best)
    #
    #     if best[1] == "distance_right_wall":  # OK
    #         # car.position.set_x(wall.rect.right)
    #         return Vector2D(wall.rect.right, y)
    #
    #     elif best[1] == "distance_left_wall":
    #         # car.position.set_x(wall.rect.left)
    #         return Vector2D(wall.rect.left - car.rect.w, y)
    #
    #     elif best[1] == "distance_bottom_wall":  # OK
    #         # car.position.set_y(wall.rect.bottom)
    #         return Vector2D(x, wall.rect.bottom)
    #
    #     else:
    #         # car.position.set_y(wall.rect.top)
    #         return Vector2D(x, wall.rect.top - car.rect.h)
    #
    # def alternate_collision_place(self,wall: Wall, car):
    #
    #     def distance(x1, y1, x2, y2):
    #         return sqrt((x1-x2)**2 + (y1 - y2)**2)
    #
    #     x,y = wall.rect.x, wall.rect.y
    #     best = float('inf')
    #     best_x, best_y = 0, 0
    #
    #     for i in range(x, x + wall.width + 1):
    #         for j in range(y, y + wall.height + 1):
    #             dist = distance(car.rect.centerx, car.rect.centery, i, j)
    #             if dist < best:
    #                 best = dist
    #                 best_x, best_y = i, j
    #
    #     best_spot = None
    #     dist2 = float('inf')
    #
    #     if distance(best_x, best_y, car.rect.x, car.rect.y) < dist2:
    #         best_spot = "top left"
    #
    #     elif distance(best_x, best_y, car.rect.x + car.width / 2, car.rect.y) < dist2:
    #         best_spot = "top front"
    #
    #     elif distance(best_x, best_y, car.rect.right, car.rect.y) < dist2:
    #         best_spot = "top right"
    #
    #     elif distance(best_x, best_y, car.rect.left, car.rect.y + car.height / 2) < dist2:
    #         best_spot = "middle left"
    #
    #     elif distance(best_x, best_y, car.rect.right, car.rect.y + car.height / 2) < dist2:
    #         best_spot = "middle right"
    #
    #     elif distance(best_x, best_y, car.rect.left, car.rect.bottom) < dist2:
    #         best_spot = "bottom left"
    #
    #     elif distance(best_x, best_y, car.rect.left + car.width / 2, car.rect.bottom) < dist2:
    #         best_spot = "bottom front"
    #
    #     elif distance(best_x, best_y, car.rect.right, car.rect.bottom) < dist2:
    #         best_spot = "bottom right"
    #
    #     return Vector2D(best_x, best_y),best_spot

    def handle_collision_with_walls(self, car):
        if car.transparent:
            return False

        collisions = pg.sprite.spritecollide(car, self.all_walls, False, pg.sprite.collide_mask)
        if collisions:  # it's a list of objects/sprites that collided with the car
            for col in collisions:
                return True

        return False

    def handle_collision_with_sufraces(self, car):
        slides = pg.sprite.spritecollide(car, self.all_surfaces, False, pg.sprite.collide_mask)
        if slides:
            for slide in slides:
                if slide.type == "FINISHLINE": #for now its kinda stupid, but the general idea is alright
                    self.stopwatch.restart_timer(pg.time.get_ticks())

                if slide.rect.x == car.rect.x + car.speed * cos(
                        radians(car.direction)) and slide.rect.y == car.rect.y + car.speed * sin(
                        radians(car.direction)):

                        return slide.adjust_fraction() #do sth about it later on!

    def handle_collision_with_boosters(self, car):
        # collisions with boosters
        pick_ups = pg.sprite.spritecollide(car, self.all_boosters, True, pg.sprite.collide_mask)  # maybe in this case it can be set to true
        if pick_ups:
            for boost in pick_ups:
                boost.activate(car, self.stopwatch)
