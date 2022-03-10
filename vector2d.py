class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add(self, x, y):
        self.x += x
        self.y += y
    def subtract(self, x, y):
        self.x -= x
        self.y -= y