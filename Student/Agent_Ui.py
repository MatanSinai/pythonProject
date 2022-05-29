from typing import List
import Agent
import pygame as pg
import threading

pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('light sky blue3')
COLOR_ACTIVE = pg.Color('dodger blue2')
FONT = pg.font.Font(None, 30)



class master_ui:

    def __init__(self, text=''):
        self.rect = pg.rect.Rect(100, 100, 140, 32)
        self.color = COLOR_INACTIVE
        self.text = text
        self.sendText = ''
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.master: Agent = None
        self.quit = False
        self.input_box = self

    def set_agent(self, master_agent):
        self.master = master_agent

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.sendText = self.text
                    self.master.name = self.sendText
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)


    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    def main_loop(self):
        clock = pg.time.Clock()

        text = FONT.render('Write your name and your password ', True, self.color)
        text2 = FONT.render('with a comma between them and no spacing', True, self.color)


        textRect = text.get_rect()
        textRect.center = (300, 50)

        text2Rect = text2.get_rect()
        text2Rect.center = (300, 75)

        while not self.quit:
            for event in pg.event.get():
                if self.sendText != '':
                    self.quit = True
                self.input_box.handle_event(event)
            self.input_box.update()
            screen.fill((30, 30, 30))
            self.input_box.draw(screen)
            screen.blit(text, textRect)
            screen.blit(text2, text2Rect)
            pg.display.flip()
            clock.tick(30)
        pg.quit()
