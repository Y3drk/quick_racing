from __future__ import annotations
import pygame as pg
from back_elements.vector2d import Vector2D

class Stopwatch (pg.sprite.Sprite):
    def __init__(self, screen, clock, position: Vector2D):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.font = pg.freetype.SysFont(None, 34)
        self.font.origin = True
        self.clock = clock
        self.x = position.x
        self.y = position.y
        self.difference = 0

    def display_timer(self, ticks):
        millis = (ticks - self.difference) % 1000
        seconds = int((ticks - self.difference) / 1000 % 60)
        minutes = int((ticks - self.difference) / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        self.font.render_to(self.screen, (self.x, self.y), out, pg.Color('black'))
        self.clock.tick(60)

    def restart_timer(self, ticks):
        self.difference = ticks
        pass

    def stop_timer(self):
        pass

    def decrease_timer(self, value: int):
        self.difference += value

    def get_time(self, ticks):
        return ticks - self.difference