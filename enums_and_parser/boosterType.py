from enum import Enum


class BoosterType(Enum):
    # both positive and negative
    SPEED = (1, "sp_resized")
    TURNING = (2, "tr_resized")

    # only positive
    NO_COLLISIONS = (3, "nw_resized")
    DECREASE_TIMER = (4, "dt_resized")

    # only negative
    NO_TURNING = (5, "nt_resized")
    FREEZE = (6, "fr_resized")
