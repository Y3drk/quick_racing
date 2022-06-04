import pygame as pg
from back_elements.map import Map
from math import sin, cos, radians

WHITE = (255, 255, 255)


class Car(pg.sprite.Sprite):
    AIR_RESISTANCE = 0.05
    TURNING_CAPABILITY = 6
    FRONT_BOUNCE = 6
    BACK_BOUNCE = 8
    FRONT_BASE_ACC = 0.1
    BACK_BASE_ACC = 0.03
    MAX_SPEED = 100

    def __init__(self, in_game_id, position, speed, direction, rotation, engine, name, curr_map: Map):
        pg.sprite.Sprite.__init__(self)
        self.id = in_game_id
        self.name = name
        self.__image = pg.image.load("./data/" + self.name + ".png").convert_alpha()
        self.image = self.__image.copy()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.position = position
        self.speed = speed
        self.direction = direction
        self.rotation = rotation
        self.engine = engine
        self.map = curr_map

        self.boosters = {"transparent": [False, 0], "speed": [0, 0], "noTurning": [False, 0],
                         "turning": [0, 0], "freeze": [False, 0]}

        self.collision_facilitator = [False, 0]

        self.mask = pg.mask.from_surface(self.image)

        self.nitro_power = 2
        self.nitro_capacity = 60
        self.nitro_duration = 40
        self.nitro_restoration_speed = 0.2

    def update(self, dt):
        self.map.handle_boosters(self)
        self.handle_collision_facilitator()

        if self.boosters["freeze"][0]:
            self.speed = 0
        else:
            collision_test_result = self.map.handle_collision_with_walls(self)

            if not collision_test_result[1]:
                self.position.add(self.speed * cos(radians(self.direction)), self.speed * sin(radians(self.direction)))
            else:
                if collision_test_result[0] == "other":
                    if self.speed * (1 + self.boosters["speed"][0]) > 0:
                        self.position.subtract((self.speed * (1 + self.boosters["speed"][0]) + Car.FRONT_BOUNCE) *
                                               cos(radians(self.direction)),
                                               (self.speed * (1 + self.boosters["speed"][0]) + Car.FRONT_BOUNCE) *
                                               sin(radians(self.direction)))
                    else:
                        self.position.add((self.speed * (1 + self.boosters["speed"][0]) + Car.BACK_BOUNCE) *
                                          cos(radians(self.direction)),
                                          (self.speed * (1 + self.boosters["speed"][0]) + Car.BACK_BOUNCE) *
                                          sin(radians(self.direction)))

                    self.speed = -(self.speed * (1 + self.boosters["speed"][0])) * Car.AIR_RESISTANCE

                    self.collision_facilitator = [True, pg.time.get_ticks() * 8]

                else:
                    self.boosters["transparent"] = [True, pg.time.get_ticks() * 40]

            self.map.handle_collision_with_surfaces(self)
            self.map.handle_collision_with_boosters(self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position.x, self.position.y

        self.mask = pg.mask.from_surface(self.image)

    def move(self, dt):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_SPACE]:
            if self.nitro_duration > 0:
                self.nitro_acceleration()
                self.nitro_duration -= 1
            else:
                self.nitro_duration = min(self.nitro_duration + self.nitro_restoration_speed, self.nitro_capacity)
        else:
            self.nitro_duration = min(self.nitro_duration + self.nitro_restoration_speed, self.nitro_capacity)
        if not self.collision_facilitator[0] and pressed[pg.K_UP]:
            self.accelerate(dt)
        if not self.collision_facilitator[0] and pressed[pg.K_DOWN]:
            self.decelerate(dt)
        if not self.boosters["noTurning"][0]:
            if pressed[pg.K_LEFT]:
                self.rotate_left(dt)
            if pressed[pg.K_RIGHT]:
                self.rotate_right(dt)

        if self.speed > 0:
            self.speed -= (self.speed * (1 + self.boosters["speed"][0])) * \
                        (Car.FRONT_BASE_ACC + (self.speed * (1 + self.boosters["speed"][0])) * 0.15 * Car.AIR_RESISTANCE)

        elif self.speed < 0:
            self.speed += (self.speed * (1 + self.boosters["speed"][0])) * \
                          (Car.BACK_BASE_ACC + (self.speed * (1 + self.boosters["speed"][0])) * Car.AIR_RESISTANCE)

        self.speed = min(self.speed, Car.MAX_SPEED)

    def rotate_left(self, dt):
        if self.speed != 0:
            self.direction = (self.direction - (Car.TURNING_CAPABILITY + self.boosters["turning"][0]) *
                              (self.speed * (1 + self.boosters["speed"][0])) * self.rotation / (dt ** 2)) % 360

            if self.direction < 0:
                self.direction += 360

            self.image = pg.transform.rotate(self.__image, 360 - self.direction)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.position.x, self.position.y
            self.mask = pg.mask.from_surface(self.image)

    def rotate_right(self, dt):
        if self.speed != 0:
            self.direction = (self.direction + (Car.TURNING_CAPABILITY + self.boosters["turning"][0]) * (
                    self.speed * (1 + self.boosters["speed"][0])) * self.rotation / (
                                      dt ** 2)) % 360
            if self.direction > 360:
                self.direction -= 360

            self.image = pg.transform.rotate(self.__image, 360 - self.direction)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.position.x, self.position.y

            self.mask = pg.mask.from_surface(self.image)

    def accelerate(self, dt):
        c = min(2, 0.3 + (self.speed / 10) ** 2)
        self.speed += self.engine * c / dt

    def decelerate(self, dt):
        self.speed -= self.engine / (2 * dt)

    def nitro_acceleration(self):
        self.speed += self.nitro_power * (lambda x: 1 if x >= 0 else -1)(self.speed)

    def handle_collision_facilitator(self):
        self.collision_facilitator[1] -= pg.time.get_ticks()
        if self.collision_facilitator[1] <= 0:
            self.collision_facilitator[0] = False
            self.collision_facilitator[1] = 0
