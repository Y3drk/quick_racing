import pygame as pg
from engine import Engine
from leaderboard import Leaderboard

white = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)

class Menu:
    #               LOGO
    #            ___________
    #           |___PLAY____|
    #           |Leaderboard|
    #           |__Settings_|
    #           |___QUIT____|
    #
    #              authors
    def __init__(self):
        pg.font.init()
        pg.init()
        self.width = 1080
        self.height = 720
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        
    def run(self):
        run = True
        while run:
            font = pg.font.SysFont('Corbel', 35)
            play_text = font.render('Play', False, white)
            play_txt = play_text.get_rect()
            play_txt.center = (540,380) #doesnt show up???
            leaderboard_text = font.render('Leaderboard', False, white)
            settings_text = font.render('Settings', False, white)
            quit_text = font.render('Quit', False, white)
            
            pos = self.pointing()
            play_color, leaderboard_color, settings_color, quit_color = color_dark, color_dark, color_dark, color_dark
            if pos == 0:
                play_color = color_light
            elif pos == 1:
                leaderboard_color = color_light
            elif pos == 2:
                settings_color = color_light
            elif pos == 3:
                quit_color = color_light
            
            pg.draw.rect(self.screen, play_color, [self.width/2 - 180, self.height/2 - 175, 360, 80])
            pg.draw.rect(self.screen, leaderboard_color, [self.width/2 - 180, self.height/2 - 85, 360, 80])
            pg.draw.rect(self.screen, settings_color, [self.width/2 - 180, self.height/2 + 5, 360, 80])
            pg.draw.rect(self.screen, quit_color, [self.width/2 - 180, self.height/2 + 95, 360, 80])
            
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pos == 0: #play button
                        print("start")
                        engine = Engine(60)
                        engine.run()
                        run = False
                    if pos == 1: #leaderboard button
                        print("leaderboard")
                        leaderboard = Leaderboard()
                        leaderboard.run()
                    if pos == 2: #settings button
                        print("settings")
                    if pos == 3: #quit button
                        run = False
                
                if event.type == pg.QUIT:
                    run = False
            pg.display.update()
    
    def pointing(self):
        pos = None
        mouse = pg.mouse.get_pos()
        if abs(mouse[0] - self.width/2) <= 180:
            if self.height/2 - 175 <= mouse[1] <= self.height/2 - 95: #play button
                pos = 0
            elif self.height/2 - 85 <= mouse[1] <= self.height/2 - 5: #leaderboard button
                pos = 1
            elif self.height/2 + 5 <= mouse[1] <= self.height/2 + 85: #settings button
                pos = 2
            elif self.height/2 + 95 <= mouse[1] <= self.height/2 + 175: #quit button
                pos = 3
        return pos

if __name__ == "__main__":
    menu = Menu()
    menu.run()