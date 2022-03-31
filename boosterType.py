from enum import Enum


class BoosterType(Enum):
    #both positive and negative
    SPEED = 1
    TURNING = 2

    #only positive
    NO_COLLISIONS = 3
    DECREASE_TIMER = 4

    #only negative
    NO_TURNING = 5
    FREEZE = 6
