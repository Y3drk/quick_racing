import pygame as pg
from engine import Engine
from leaderboard import Leaderboard
from settings import Settings

white = (255,255,255)
color_light = (100, 200, 255)
color_dark = (170,170,170)

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
        self.settings = Settings()
        
    def run(self):
        background = pg.image.load("./data/background_beg.png")
        background = pg.transform.scale(background, (self.width, self.height))
        run = True
        while run: 
            self.screen.blit(background, (0,0))
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
            
            pb = pg.draw.rect(self.screen, play_color, [self.width/2 - 180, self.height/2 - 175, 360, 80])
            pg.draw.rect(self.screen, (0,0,0), pb, 2)
            lb = pg.draw.rect(self.screen, leaderboard_color, [self.width/2 - 180, self.height/2 - 85, 360, 80])
            pg.draw.rect(self.screen, (0,0,0), lb, 2)
            sb = pg.draw.rect(self.screen, settings_color, [self.width/2 - 180, self.height/2 + 5, 360, 80])
            pg.draw.rect(self.screen, (0,0,0), sb, 2)
            qb = pg.draw.rect(self.screen, quit_color, [self.width/2 - 180, self.height/2 + 95, 360, 80])
            pg.draw.rect(self.screen, (0,0,0), qb, 2)
            
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pos == 0: #play button
                        name, car, map = self.settings.get_settings()
                        engine = Engine(60, name, car, map)
                        run = False
                        engine.run()
                        run = True
                    if pos == 1: #leaderboard button
                        leaderboard = Leaderboard()
                        run = False
                        leaderboard.run()
                        run = True
                    if pos == 2: #settings button
                        run = False
                        self.settings.run()
                        run = True
                    if pos == 3: #quit button
                        run = False
                
                if event.type == pg.QUIT:
                    run = False
                    
            font = pg.font.SysFont('Calibri', 35)
            
            play_text = font.render("Play", 1, (0,0,0))
            self.screen.blit(play_text, play_text.get_rect(center = pb.center))
            leaderboard_text = font.render("Leaderboard", 1, (0,0,0))
            self.screen.blit(leaderboard_text, leaderboard_text.get_rect(center = lb.center))
            settings_text = font.render("Settings", 1, (0,0,0))
            self.screen.blit(settings_text, settings_text.get_rect(center = sb.center))
            quit_text = font.render("Quit", 1, (0,0,0))
            self.screen.blit(quit_text, quit_text.get_rect(center = qb.center))
            
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