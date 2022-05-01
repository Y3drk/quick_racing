import pygame as pg

class Settings:
    def __init__(self):
        pg.init()
        self.width = 1080
        self.height = 720
        self.screen = pg.display.set_mode((self.width, self.height))
        self.font = pg.font.SysFont('Calibri', 35)
        self.text_input = pg.Rect(self.width // 2 - 500, 50, 1000, 80)
        self.text_input_header = pg.Rect(self.width // 2 - 500, 10, 1000, 30)
        self.name = ""
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
    
    def run(self):
        background = pg.image.load("./data/settings_bg.png")
        background = pg.transform.scale(background, (self.width, self.height))
        run = True
        while run:
            self.screen.blit(background,(0,0))
            
            current_name = self.font.render(self.name, 1, (0,0,0))
            self.screen.blit(current_name, current_name.get_rect(center = self.text_input.center))
            pg.draw.rect(current_name, (100,200,255), [self.width // 2 - 500, 50, 1000, 80])
            pg.draw.rect(self.screen, (0,0,0), self.text_input, 2)
            
            your_name_text = self.font.render("Your name:", 1, (0,0,0))
            self.screen.blit(your_name_text, your_name_text.get_rect(center = self.text_input_header.center))
            your_name = pg.draw.rect(your_name_text, (100,200,255), [self.width // 2 - 500, 10, 1000, 30])
            
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    active = self.text_input.collidepoint(event.pos)
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            print(self.name)
                        elif event.key == pg.K_BACKSPACE:
                            self.name = self.name[:-1]
                        elif len(self.name) < 50:
                            self.name += event.unicode
                
                if event.type == pg.QUIT:
                    run = False
            pg.display.update()
        
if __name__ == "__main__":
    settings = Settings()
    settings.run()