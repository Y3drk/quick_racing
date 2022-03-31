import pygame as pg

white = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)

class Leaderboard:
    def __init__(self):
        pg.init()
        self.width = 1080
        self.height = 720
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        
    def run(self):
        run = True
        while run:
            for event in pg.event.get():
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
    leaderboard = Leaderboard()
    leaderboard.run()