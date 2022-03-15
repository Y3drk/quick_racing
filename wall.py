from vector2d import Vector2D


class Wall:
    def __init__(self, lower_left_corner: Vector2D, upper_right_corner: Vector2D):
        self.lower_left_corner = lower_left_corner
        self.upper_right_corner = upper_right_corner  #for now it's a rectangle
        self.height = (upper_right_corner.subtract_vector(lower_left_corner)).y
        self.length = (upper_right_corner.subtract_vector(lower_left_corner)).x