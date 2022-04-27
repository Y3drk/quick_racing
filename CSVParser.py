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
            row.append(row)

        #planned CSV structure ->
        #0 type(string -> what is it, wall / surface),
        #1 position x,
        #2 position y,
        #3 width,
        #4 height,
        #5 surfaceType or with_tires to specify
        for row in rows:
            position = Vector2D(row[1], row[2])
            width = row[3]
            height = row[4]

            if row[0] == "WALL":
                if row[5] == "with_tires":
                    map.walls.append(Wall(position, width, height, True))
                else:
                    map.walls.append(Wall(position, width, height, False))

            elif row[0] == "SURFACE":
                if row[5] == "ASPHALT":
                    map.sufraces.append(Surface(position, width, height, SurfaceType.ASPHALT))

                elif row[5] == "SNOW":
                    map.sufraces.append(Surface(position, width, height, SurfaceType.SNOW))

                elif row[5] == "ICE":
                    map.sufraces.append(Surface(position, width, height, SurfaceType.ICE))

                elif row[5] == "GRAVEL":
                    map.sufraces.append(Surface(position, width, height, SurfaceType.GRAVEL))

                elif row[5] == "SAND":
                    map.sufraces.append(Surface(position, width, height, SurfaceType.SAND))

                elif row[5] == "GRASS":
                    map.sufraces.append(Surface(position, width, height, SurfaceType.GRASS))

                elif row[5] == "FINISHLINE":
                    map.sufraces.append(Surface(position, width, height, SurfaceType.FINISHLINE))

        file.close()

    def write_to_leaderboard(self):
        file = open(self.leaderboard)
        csv_writer = csv.writer(file)
        file.close()