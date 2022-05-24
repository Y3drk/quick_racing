
from back_elements.wall import Wall
from back_elements.surface import Surface
from enums_and_parser.surfaceType import SurfaceType
import csv
from back_elements.vector2d import Vector2D


class CSVParser:
    def __init__(self, map_source, leaderboard, cars):
        self.source_file = map_source
        self.leaderboard = leaderboard
        self.cars = cars

    def draw_map(self, map):
        file = open(self.source_file)
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        rows = []

        for row in csv_reader:
            rows.append(row)

        #planned CSV structure ->
        #0 type(string -> what is it, wall / surface),
        #1 position x,
        #2 position y,
        #3 width,
        #4 height,
        #5 surfaceType or with_tires to specify
        #6 rotation -> if it has image, how much is it rotated
        for row in rows:
            position = Vector2D(int(row[1]), int(row[2]))
            width = int(row[3])
            height = int(row[4])
            rotation = int(row[6])

            if row[0] == "WALL":
                if row[5] == "WITH_TIRES":
                    map.all_walls.add(Wall(position, width, height, True, rotation))
                else:
                    map.all_walls.add(Wall(position, width, height, False, rotation))

            elif row[0] == "SURFACE":
                if row[5] == "ASPHALT":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.ASPHALT, rotation))
                    map.places_for_boosters.append([position.x + 40, position.y + 40, position.x + width - 40, position.y + height - 40])

                elif row[5] == "SNOW":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.SNOW, rotation))

                elif row[5] == "ICE":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.ICE, rotation))

                elif row[5] == "GRAVEL":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.GRAVEL, rotation))

                elif row[5] == "SAND":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.SAND, rotation))

                elif row[5] == "GRASS":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.GRASS, rotation))

                elif row[5] == "FINISHLINE":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.FINISHLINE, rotation))

                elif row[5] == "SIDE":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.SIDE, rotation))

                elif row[5] == "CHECKPOINT":
                    map.all_surfaces.add(Surface(position, width, height, SurfaceType.CHECKPOINT, rotation))
                    map.checkpoints.append(False)

        file.close()

    def write_to_leaderboard(self,result, name, map, car):
        #assuming the following schema of the CSV file:
        #0 - player name
        #1 - player result(time)
        #2 - map
        #3 - car model

        file = open(self.leaderboard)
        csv_writer = csv.writer(file)
        new_row = [name, result, map.name, car.name]
        csv_writer.writerow(new_row)

        file.close()

    def read_leaderboard(self):
        file = open(self.leaderboard)
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        rows = []

        for row in csv_reader:
            row.append(row)

        #now we can do what we want with the rows - it's up to us what

        file.close()
        pass

    def read_car_statistics(self, car_id:int):
        #planned cars file structure:
        #[0] - id
        #[1] - NAME
        #[2] - engine

        file = open(self.cars)
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        rows = []

        for row in csv_reader:
            rows.append(row)

        #we return this data to engine or whatever and it will create a car
        return int(rows[car_id][0]), rows[car_id][1], int(rows[car_id][2])
