import pygame as pg
from vector2d import Vector2D
from car import Car
from map import Map
from wall import Wall
from math import sqrt

#TODO
def choose_collision_place(x, y, wall: Wall):
    closest_distance = float('inf')
    chosen_block_place = None
    #print(wall.rect.top, wall.rect.topleft, wall.rect.centerx, wall.rect.center)

    distance = sqrt((x - wall.rect.topleft[0])**2 + (y - wall.rect.topleft[1]))
    if closest_distance < distance:
        closest_distance = distance
        chosen_block_place = wall.rect.topleft

    #wrong
    distance = sqrt((x - wall.rect.top[1])**2 + (y - wall.rect.top[1]))
    if closest_distance < distance:
        closest_distance = distance
        chosen_block_place = wall.rect.top

    distance = sqrt((x - wall.rect.topright[0])**2 + (y - wall.rect.topright[1]))
    if closest_distance < distance:
        closest_distance = distance
        chosen_block_place = wall.rect.topright

    distance = sqrt((x - (wall.rect.bottomright[0] - wall.rect.bottomleft[0])**2 + (y - wall.rect.bottomright[1] - wall.rect.bottomleft[1])))
    if closest_distance < distance:
        closest_distance = distance
        chosen_block_place = wall.rect.right

    distance = sqrt((x - wall.rect.bottomright[0])**2 + (y - wall.rect.bottomright[1]))
    if closest_distance < distance:
        closest_distance = distance
        chosen_block_place = wall.rect.bottomright

    #wrong
    distance = sqrt((x - wall.rect.bottom[1])**2 + (y - wall.rect.bottom[1]))
    if closest_distance < distance:
        closest_distance = distance
        chosen_block_place = wall.rect.bottom

    return chosen_block_place

class Engine:
    def __init__(self, refresh_rate):
        self.refresh = refresh_rate
        pg.init()
        self.screen = pg.display.set_mode((400,300))
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        self.clock = pg.time.Clock()
        self.all_walls = pg.sprite.Group()
    # btw that's how we can load the map -> read all walls size and location from CSV then create
    # them and add them all to sprite group,
    # same probably could be done with ground types -> we can also handle fraction using collisions :)
    # also I think it would be beneficial if all_walls were an attribute of the map

    def run(self):
        wall1 = Wall(Vector2D(40, 40), 20, 20)
        self.all_walls.add(wall1) # beginning of sprites

        car = Car(0, Vector2D(10, 10), 0, 0, 60, 30)
        # car_img = pg.image.load("./data/car.png") #done temporarily inside the car class
        map = Map(0, 1000, 300, car, None)
        map_img = pg.image.load("./data/grass.png")
        run = True


        while run:
            dt = self.clock.tick(self.refresh)
            self.screen.blit(map_img, (0, 0))
            self.screen.blit(car.image, (car.position.x, car.position.y))
            #self.all_cars.draw(self.screen)
            #added
            self.all_walls.draw(self.screen)

            # pressed = pg.key.get_pressed()
            # if pressed[pg.K_UP]:
            #     car.accelerate(dt)
            # if pressed[pg.K_DOWN]:
            #     car.decelerate(dt)
            # if pressed[pg.K_LEFT]:
            #     car.rotate_left(dt)
            # if pressed[pg.K_RIGHT]:
            #     car.rotate_right(dt)

            car.update(dt)
            car.move(dt) # maybe car also should be coded as a sprite???
            self.all_walls.update()

            collisions = pg.sprite.spritecollide(car, self.all_walls, False)

            if collisions: # it's a list of objects/sprites that collided with the car
                print(collisions)
                car.speed = 0 # well the setter is needed
                car.position = Vector2D(collisions[0].rect.bottomright[0], collisions[0].rect.bottomright[1])

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            pg.display.flip()


def main():
    #choose_collision_place(0, 0, Wall(Vector2D(40, 40), 20, 20))
    engine = Engine(60)
    engine.run()

if __name__ == "__main__":
    main()