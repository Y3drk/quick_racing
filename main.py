import pygame as pg
from vector2d import Vector2D
from car import Car
from map import Map
from wall import Wall

#TODO

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

    print(best)

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
        wall1 = Wall(Vector2D(150, 150), 60, 60)
        self.all_walls.add(wall1) # beginning of sprites

        traction = 0.15

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


            car.update(dt)
            car.move(dt) # maybe car also should be coded as a sprite???
            self.all_walls.update()

            collisions = pg.sprite.spritecollide(car, self.all_walls, False)

            if collisions: # it's a list of objects/sprites that collided with the car
                print(collisions)
                car.position = new_collision_place(car.position.x, car.position.y, collisions[0], car)
                car.speed = -car.speed * traction   # well the setter is needed


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            pg.display.flip()


def main():
    #print(choose_collision_place(0, 0, Wall(Vector2D(40, 40), 20, 20)))
    engine = Engine(60)
    engine.run()

if __name__ == "__main__":
    main()