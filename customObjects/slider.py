import pygame
from customObjects import custom_text

class Slider:
    def __init__(self, display, x, y, width, height, min_value=0.0, max_value=1.0,
                 initial_value=0.5, label=None, on_change=None):
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label_text = label
        self.on_change = on_change
        self.dragging = False

        self.handle_width = 20
        self.handle_height = height + 10

        # Add slider to display objects
        self.display.objects.append(self)

        # Create label
        if self.label_text:
            self.label = custom_text.Custom_text(
                self.display,
                x + self.width / 2,
                y - self.handle_height,
                f"{self.label_text}: {int(self.value * 100)}%",
                text_color="white"
            )


    def get_handle_position(self):
        normalized = (self.value - self.min_value) / (self.max_value - self.min_value)
        return self.x + normalized * (self.width - self.handle_width)

    def set_value_from_position(self, x_pos):
        x_pos = max(self.x + self.handle_width / 2, min(x_pos, self.x + self.width - self.handle_width / 2))
        normalized_pos = (x_pos - self.x - self.handle_width / 2) / (self.width - self.handle_width)
        new_value = self.min_value + normalized_pos * (self.max_value - self.min_value)

        if new_value != self.value:
            self.value = new_value
            self.update_label()
            if self.on_change:
                self.on_change(self.value)

    def update_label(self):
        if hasattr(self, 'label'):
            self.label.update_text(f"{self.label_text}: {int(self.value * 100)}%")

    def events(self, event):
        handle_x = self.get_handle_position()
        handle_rect = pygame.Rect(handle_x, self.y - 5, self.handle_width, self.handle_height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if click is on handle
            if handle_rect.collidepoint((mouse_x, mouse_y)):
                self.dragging = True
            # Also allow clicking on the track to move the handle
            elif (self.x <= mouse_x <= self.x + self.width and
                  self.y <= mouse_y <= self.y + self.height):
                self.dragging = True
                self.set_value_from_position(mouse_x)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            self.set_value_from_position(mouse_x)

    def render(self):
        screen = self.display.screen

        track_color = (150, 150, 150)
        handle_color = (0, 255, 0)
        filled_color = (0, 200, 0)

        pygame.draw.rect(screen, track_color, (self.x, self.y, self.width, self.height))

        handle_x = self.get_handle_position()

        filled_width = handle_x + self.handle_width / 2 - self.x
        pygame.draw.rect(screen, filled_color, (self.x, self.y, filled_width, self.height))

        pygame.draw.rect(screen, handle_color,
                         (handle_x, self.y - 5, self.handle_width, self.handle_height))

        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height), 1)