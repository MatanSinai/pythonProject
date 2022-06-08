from typing import List
import Agents_Manager
import pygame as pg
import threading
from tkinter import *
from tkinter import filedialog

pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('light sky blue3')
COLOR_ACTIVE = pg.Color('dodger blue2')
FONT = pg.font.Font(None, 32)
FONT2 = pg.font.Font(None, 25)



class master_ui:

    def __init__(self, text=''):
        self.rect = pg.rect.Rect(100, 100, 140, 32)
        self.color = COLOR_INACTIVE
        self.text = text
        self.sendText = ''
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.master: Agents_Manager = None
        self.quit = False
        self.input_box = self

    def run(self):
        x = threading.Thread(target=self.activate(), args=())
        x.start()

    #get Agent and put into my variable master
    def set_master_socket(self, master_socket):
        self.master = master_socket

    #update sendText with the the file path
    def openFile(self):
        self.sendText = filedialog.askopenfilename()

    #open file explorer and let you choose the file path
    def loop_file(self):
        window = Tk()
        self.openFile()
        window.destroy()
        window.mainloop()

    #recive the keys from the keyboard and mouse and update the sendText and text
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
                    if self.sendText == 'file':
                        self.master.message_everyone('file')
                        print("file")
                        self.loop_file()
                        print(self.sendText)
                        if self.sendText.split(".")[-1] == 'xlsx':
                            self.master.message_everyone('xlsx')

                        elif self.sendText.split(".")[-1] == 'docx':
                            self.master.message_everyone('docx')

                        elif self.sendText.split(".")[-1] == 'pptx':
                            self.master.message_everyone('pptx')

                        self.master.send_file(self.sendText)
                    elif self.sendText == 'close program':
                        print("close")
                        self.quit = True
                        self.master.quit = True
                        self.master.message_everyone(self.sendText)

                    elif self.sendText == 'close all':
                        self.master.message_everyone(self.sendText)
                    else:
                        self.master.message_everyone(self.sendText)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    # Resize the box if the text is too long.
    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    #draw the screen
    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    #run the whole graphic of the manager
    def activate(self):
        clock = pg.time.Clock()

        text = FONT.render('Write What you would like to open', True, self.color)
        textRect = text.get_rect()
        textRect.center = (275, 50)

        text_user_name = FONT.render('Connected clients', True, self.color)
        user_name_rect = text_user_name.get_rect()
        user_name_rect.center = (300, 200)


        while not self.quit:
            for event in pg.event.get():
                self.input_box.handle_event(event)
            self.input_box.update()
            screen.fill((30, 30, 30))
            self.input_box.draw(screen)
            screen.blit(text, textRect)
            screen.blit(text_user_name, user_name_rect)
            names = list(self.master.user_name.values())
            text_names = FONT2.render(str(names), True, self.color)
            print_names_rect = text_names.get_rect()
            print_names_rect.center = (300, 300)
            screen.blit(text_names, print_names_rect)
            pg.display.flip()
            clock.tick(30)
        self.master.quit = True
        pg.quit()
