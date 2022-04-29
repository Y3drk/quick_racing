from enum import Enum


class BoosterType(Enum):
    #both positive and negative
    SPEED = (1, (255, 255, 255))
    TURNING = (2, (255, 255, 255))

    #only positive
    NO_COLLISIONS = (3, (255, 255, 255))
    DECREASE_TIMER = (4, "dt_resized")

    #only negative
    NO_TURNING = (5, (255, 255, 255))
    FREEZE = (6, (255, 255, 255))
