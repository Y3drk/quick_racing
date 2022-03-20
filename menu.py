import pygame as pg

class Menu:
    
    #               LOGO
    #            ___________
    #           |___PLAY____|
    #           |Leaderboard|
    #           |__Settings_|
    #
    #              authors
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1080,720))
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        self.clock = pg.time.Clock()
        