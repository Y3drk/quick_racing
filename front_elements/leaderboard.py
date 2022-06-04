import pygame as pg
import csv

white = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)


class OptionBox():
    def __init__(self, x, y, width, height, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pg.Rect(x, y, width, height)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pg.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pg.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))
        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pg.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pg.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event):
        mouse_position = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mouse_position)
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mouse_position):
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


class Leaderboard:
    def __init__(self):
        pg.init()
        self.width = 1080
        self.height = 720
        self.screen = pg.display.set_mode((self.width, self.height))
        self.car = 0
        self.map = 0
        self.font = pg.font.SysFont('Calibri', 35)
        self.cars_options = OptionBox(680, 40, 160, 40, (240, 230, 140), (100, 200, 255), self.font,
                                      ["car 1", "car 2", "car 3"])
        self.maps_options = OptionBox(880, 40, 160, 40, (240, 230, 140), (100, 200, 255), self.font,
                                      ["map 1", "map 2", "map 3"])
        w = 490
        h = 90
        self.scores = [pg.Rect(100, 100, w, h), pg.Rect(100, 200, w, h), pg.Rect(100, 300, w, h),
                       pg.Rect(100, 400, w, h), pg.Rect(100, 500, w, h)]
        self.quit_button = pg.draw.rect(self.screen, (100, 200, 255), [self.width - 400, self.height - 120, 360, 80], 1)
        pg.display.update()
        pg.display.set_caption("QUICK RACING")

    def run(self):
        background = pg.image.load("data/leaderboard_bg.png")
        background = pg.transform.scale(background, (self.width, self.height))
        self.records = self.get_leaderboard()
        quit_color = (100, 200, 255)
        run = True
        while run:
            self.screen.blit(background, (0, 0))

            self.quit_button = pg.draw.rect(self.screen, quit_color, [self.width - 400, self.height - 120, 360, 80])
            pg.draw.rect(self.screen, (0, 0, 0), self.quit_button, 2)
            if self.pointing():
                quit_color = (100, 200, 255)
            else:
                quit_color = (240, 230, 140)
            quit = self.font.render("Quit", 1, (0, 0, 0))
            self.screen.blit(quit, quit.get_rect(center=self.quit_button.center))

            self.cars_options.draw(self.screen)
            self.maps_options.draw(self.screen)
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN and self.pointing():
                    run = False
                    self.screen.fill((0, 0, 0))
                car_selected_option = self.cars_options.update(event)
                if car_selected_option >= 0:
                    self.car = car_selected_option
                    self.records = self.get_leaderboard()
                map_selected_option = self.maps_options.update(event)
                if map_selected_option >= 0:
                    self.map = map_selected_option
                    self.records = self.get_leaderboard()
                if event.type == pg.QUIT:
                    run = False

            for i in range(5):
                pg.draw.rect(self.screen, (240, 230, 140), self.scores[i])
                pg.draw.rect(self.screen, (0, 0, 0), self.scores[i], 2)
                if len(self.records) <= i:
                    msg = self.font.render("-", 1, (0, 0, 0))
                else:
                    millis = self.records[i][2] % 1000
                    seconds = int(self.records[i][2] / 1000 % 60)
                    minutes = int(self.records[i][2] / 60000 % 24)
                    t = "{minutes:02d}.{seconds:02d}.{millis}".format(minutes=minutes, millis=millis, seconds=seconds)
                    msg = self.font.render(self.records[i][3] + ": " + t, 1, (0, 0, 0))
                self.screen.blit(msg, msg.get_rect(center=self.scores[i].center))

            pg.display.update()

    def pointing(self):
        mouse = pg.mouse.get_pos()
        return (self.width - 400 <= mouse[0] <= self.width - 40) and (self.height - 120 <= mouse[1] <= self.height - 40)

    def get_leaderboard(self):
        records = []
        with open("data/Records.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "supra_new":
                    car = 0
                elif row[0] == "ferrari458":
                    car = 1
                else:
                    car = 2
                if row[1] == "map1":
                    map = 0
                elif row[1] == "map2":
                    map = 1
                else:
                    map = 2
                if car == self.car and map == self.map:
                    row[2] = int(row[2])
                    records.append(row)
        records.sort(key=lambda x: x[2])
        if len(records) > 5:
            return records[:5]
        else:
            return records


if __name__ == "__main__":
    leaderboard = Leaderboard()
    leaderboard.run()
