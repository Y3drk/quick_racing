import pygame as pg

class OptionBox():
    def __init__(self,x,y,w,h,color,highlight_color,option_list,selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pg.Rect(x,y,w,h)
        self.font = pg.font.SysFont('Calibri', 35)
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
    def draw(self, surf):
        pg.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pg.draw.rect(surf, (0,0,0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0,0,0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))
        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pg.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0,0,0))
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pg.draw.rect(surf, (0,0,0), outer_rect, 2)
    def update(self, event):
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break
        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.selected = self.active_option
                self.draw_menu = False
                return self.active_option
        return -1

class Settings:
    def __init__(self):
        pg.init()
        self.width = 1080
        self.height = 720
        self.screen = pg.display.set_mode((self.width, self.height))
        self.font = pg.font.SysFont('Calibri', 35)
        self.text_input = pg.Rect(self.width // 2 - 500, 50, 1000, 80)
        self.text_input_header = pg.Rect(self.width // 2 - 500, 10, 1000, 30)
        self.name = "Player 1"
        
        self.cars_options = OptionBox(self.width//2 - 300, 200, 200, 50, (240,230,140), (100,100,255), ["car 1", "car 2", "car 3"])
        self.maps_options = OptionBox(self.width//2 + 100, 200, 200, 50, (240,230,140), (100,100,255), ["map 1", "map 2", "map 3"])
        self.car = 0
        self.map = 0
        
        self.save_button = pg.draw.rect(self.screen, (240,230,140), [self.width//2 - 100, 500, 200, 50])
        pg.draw.rect(self.screen, (0,0,0), self.save_button, 2)
        
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
            
            self.cars_options.draw(self.screen)
            self.maps_options.draw(self.screen)
            
            
            if self.save_button.collidepoint(pg.mouse.get_pos()):
                color = (100,100,255)
            else:
                color = (240,230,140)
            self.save_button = pg.draw.rect(self.screen, color, [self.width//2 - 100, 500, 200, 50])
            pg.draw.rect(self.screen, (0,0,0), self.save_button, 2)
            save_text = self.font.render("Save", 1, (0,0,0))
            self.screen.blit(save_text, save_text.get_rect(center = self.save_button.center))
            
            for event in pg.event.get():
                car_selected_option = self.cars_options.update(event)
                if car_selected_option >= 0:
                    self.car = car_selected_option
                map_selected_option = self.maps_options.update(event)
                if map_selected_option >= 0:
                    self.car = map_selected_option
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
                
                if event.type == pg.MOUSEBUTTONDOWN and self.save_button.collidepoint(event.pos):
                    run = False
                if event.type == pg.QUIT:
                    run = False
            pg.display.update()
        
if __name__ == "__main__":
    settings = Settings()
    settings.run()