import map
from wall import Wall
from surface import Surface
from surfaceType import SurfaceType
import csv
from vector2d import Vector2D


class CSVParser:
    def __init__(self, map_source, leaderboard):
        self.source_file = map_source
        self.leaderboard = leaderboard

    def draw_map(self, map: map):
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