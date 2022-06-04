from enum import Enum


class SurfaceType(Enum):
    ASPHALT = (0.9, (0, 0, 0))  # (fraction, colour) respectively
    SNOW = (0.35, (245, 245, 245))
    ICE = (0.1, (153, 204, 255))
    GRAVEL = (0.4, (204, 102, 0))
    GRASS = (0.5, (0, 204, 0))
    SAND = (0.25, (255, 255, 0))
    FINISHLINE = (0.9, "./data/finish_line.png")
    SIDE = (0.9, "./data/side.png")
    CHECKPOINT = (0.9, (255, 0, 0))
