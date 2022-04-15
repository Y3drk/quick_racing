import pygame as pg
import csv

white = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)

class OptionBox():
	def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
		self.color = color
		self.highlight_color = highlight_color
		self.rect = pg.Rect(x, y, w, h)
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
		surf.blit(msg, msg.get_rect(center = self.rect.center))

		if self.draw_menu:
			for i, text in enumerate(self.option_list):
				rect = self.rect.copy()
				rect.y += (i+1) * self.rect.height
				pg.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
				msg = self.font.render(text, 1, (0, 0, 0))
				surf.blit(msg, msg.get_rect(center = rect.center))
			outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
			pg.draw.rect(surf, (0, 0, 0), outer_rect, 2)

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

class Leaderboard:
	def __init__(self):
		pg.init()
		self.width = 1080
		self.height = 720
		self.screen = pg.display.set_mode((self.width, self.height))
		self.car = "car 1" #temp name
		self.map = "map 1" #temp name
		self.cars_options = OptionBox( 40, 40, 160, 40, (150, 150, 150), (100, 200, 255), pg.font.SysFont('Corbel', 35), 
								["car 1", "car 2", "car 3"])
		self.maps_options = OptionBox( 40, 40, 160, 40, (150, 150, 150), (100, 200, 255), pg.font.SysFont('Corbel', 35), 
								["map 1", "map 2", "map 3"])
		pg.display.update()
		pg.display.set_caption("QUICK RACING")
		
	def run(self):
		records = self.get_leaderboard()
		run = True
		while run:
			for event in pg.event.get():
				selected_option = self.cars_options.update(event)
				if selected_option >= 0:
					print(selected_option)
				if event.type == pg.QUIT:
					run = False
			self.cars_options.draw(self.screen)
   			self.maps_options.draw(self.screen)
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

	def get_leaderboard(self):
		records = []
		with open("./data/records.csv", "r") as f:
			reader = csv.reader(f)
			for row in reader:
				if row[0] == self.car and row[1] == self.map:
					records.append(row.sort(key = lambda x: x[2]))
		return records[:5]

if __name__ == "__main__":
	leaderboard = Leaderboard()
	leaderboard.run()