from enum import Enum

class SurfaceType(Enum):
    #in car.move there is friction hardcoded so it will be easy to add these values
    #but we can also consider adding air friction - wind (given we have enough time)
    #it would be similar but it would depend on direction of movement 
    ASPHALT = (0.9, (0, 0, 0))  # (fraction, colour) respectively
    SNOW = (0.35, (255, 255, 255))
    ICE = (0.1, (153, 204, 255))
    GRAVEL = (0.4, (204, 102, 0))
    GRASS = (0.5, (0, 204, 0))
    SAND = (0.25, (255, 255, 0))
    FINISHLINE = (0.9, "finish_line.png") #special case where there will be an image
