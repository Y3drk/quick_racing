from __future__ import annotations
import pygame as pg
from vector2d import Vector2D
from car import Car
from map import Map
from wall import Wall
from surface import Surface
from surfaceType import SurfaceType
from stopwatch import Stopwatch


def new_collision_place(x,y, wall: Wall, car : Car):
    options = []

    distance_right_wall = abs(x - wall.rect.right)
    options.append((distance_right_wall, "distance_right_wall"))

    distance_left_wall = abs(x - wall.rect.left)
    options.append((distance_left_wall, "distance_left_wall"))

    distance_bottom_wall = abs(y - wall.rect.bottom)
    options.append((distance_bottom_wall, "distance_bottom_wall"))

    distance_top_wall = abs(y - wall.rect.top)
    options.append((distance_top_wall, "distance_top_wall"))

    best = (float('inf'), None)
    for dist in options:
        if best[0] > dist[0]:
            best = dist

    #print(best)

    if best[1] == "distance_right_wall":  # OK
        #car.position.set_x(wall.rect.right)
        return Vector2D(wall.rect.right, y)

    elif best[1] == "distance_left_wall":
        #car.position.set_x(wall.rect.left)
        return Vector2D(wall.rect.left - car.rect.w, y)

    elif best[1] == "distance_bottom_wall": # OK
        #car.position.set_y(wall.rect.bottom)
        return Vector2D(x, wall.rect.bottom)

    else:
        #car.position.set_y(wall.rect.top)
        return Vector2D(x, wall.rect.top - car.rect.h)


class Engine:
    def __init__(self, refresh_rate):
        self.refresh = refresh_rate
        pg.init()
        self.screen = pg.display.set_mode()
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        self.clock = pg.time.Clock()
        self.all_walls = pg.sprite.Group()
        self.all_surfaces = pg.sprite.Group()

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
        wall1 = Wall(Vector2D(250, 300), 60, 60, False)
        self.all_walls.add(wall1) # beginning of sprites
        wall2 = Wall(Vector2D(20, 150), 60, 20, True)
        self.all_walls.add(wall2)  # beginning of sprites

        surface1 = Surface(Vector2D(150, 20), 100, 50, SurfaceType.ASPHALT)
        self.all_surfaces.add(surface1)
        surface2 = Surface(Vector2D(400, 200), 100, 80, SurfaceType.ICE)
        self.all_surfaces.add(surface2)


        traction = 0.15

        car = Car(0, Vector2D(10, 10), 0, 0, 10, 200)
        # car_img = pg.image.load("./data/car.png") #done temporarily inside the car class
        x, y = self.screen.get_size()
        curr_map = Map(0, x, y, car, None, None)
        map_img = pg.image.load("./data/grass.png")
        run = True
        stopwatch = self.start_timer()

        while run:
            dt = self.clock.tick(self.refresh)
            self.screen.blit(map_img, (0, 0))

            self.all_surfaces.draw(self.screen)
            self.all_surfaces.update()

            #self.screen.blit(car.image, (car.position.x, car.position.y))
            #self.all_cars.draw(self.screen)
            #added

            self.all_walls.draw(self.screen)
            self.all_walls.update()

            car.update(dt)
            car.move(dt) # maybe car also should be coded as a sprite???

            self.screen.blit(car.image, (car.position.x, car.position.y))

            collisions = pg.sprite.spritecollide(car, self.all_walls, False)
            if collisions: # it's a list of objects/sprites that collided with the car
                for col in collisions:
                    car.position = new_collision_place(car.position.x, car.position.y, col, car)
                    car.speed = -car.speed * traction   # well the setter is needed

            slides = pg.sprite.spritecollide(car, self.all_surfaces, False)
            if slides:
                #print("surface here")
                for slide in slides:
                    traction = slide.adjust_fraction()

            #print(traction) no we have to include different surfaces in the movement of the car

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            ticks = pg.time.get_ticks()
            stopwatch.display_timer(ticks)


            pg.display.flip()