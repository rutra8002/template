import pygame
from customObjects import custom_text


class Button:  # A button class
    def __init__(self, display, action, x, y, width, height, color=(255, 255, 255), text=None, text_color='black', outline_color=None, outline_width=5, append=True):  # Getting all the parameters of the button

        self.action = action
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.append = append
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Creating a rect object

        self.display.objects_in_memory += 1
        if self.append:
            self.display.objects.append(self)  # Adding self to objects of the screen

        if text != None:  # if there is text it's put on the button
            self.text = custom_text.Custom_text(self.display, self.x + self.width / 2, self.y + self.height / 2,text,  font="fonts/VCR_OSD_MONO.ttf", font_height=self.height // 2, text_color=text_color)

        self.outline_color = outline_color
        self.outline_width = outline_width

    def render(self):  # Rendering a button on screen
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.display.screen, self.get_hover_color(), self.rect, border_radius=0)
        else:
            pygame.draw.rect(self.display.screen, self.color, self.rect, border_radius=0)


        if self.outline_color != None:
            pygame.draw.rect(self.display.screen, self.outline_color, self.rect, self.outline_width, border_radius=0)

    def events(self, event):  # Checks events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            if callable(self.action):
                self.action()
            else:
                print('No valid action assigned to this button')

    def delete(self):
        self.text.delete()
        self.display.objects_in_memory -= 1
        if self.append:
            self.display.objects.remove(self.text)
        del self

    def get_hover_color(self):
        biggest = max(self.color)
        if biggest <= 225:
            return tuple(color + 30 for color in self.color)
        else:
            return tuple(color - 30 if color >= 30 else 0 for color in self.color)

    def update_color(self, color):
        self.outline_color = color
        self.text.update_color(color, None)
