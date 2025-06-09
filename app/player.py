import pygame
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.width = 50
        self.height = 50
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.w = self.a = self.d = self.s = self.space = False
        self.speed = 6000 # roughly 4.69 times more than actual speed when 0.01 friction
        self.friction = 0.01
        self.angle = 0

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (255, 0, 0), (0, 0, self.width, self.height))


    def render(self):
        rotated_surface = pygame.transform.rotate(self.surface,
                                                  -self.angle)
        rect = rotated_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        self.game.screen.blit(rotated_surface, rect.topleft)
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.w = True
            elif event.key == pygame.K_s:
                self.s = True
            elif event.key == pygame.K_a:
                self.a = True
            elif event.key == pygame.K_d:
                self.d = True
            elif event.key == pygame.K_SPACE:
                self.space = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.w = False
            elif event.key == pygame.K_s:
                self.s = False
            elif event.key == pygame.K_a:
                self.a = False
            elif event.key == pygame.K_d:
                self.d = False
            elif event.key == pygame.K_SPACE:
                self.space = False


    def update(self):
        if self.w:
            self.vy -= self.speed * self.game.delta_time
        if self.s:
            self.vy += self.speed * self.game.delta_time
        if self.a:
            self.vx -= self.speed * self.game.delta_time
        if self.d:
            self.vx += self.speed * self.game.delta_time

        friction_factor = self.friction ** self.game.delta_time
        self.vx *= friction_factor
        self.vy *= friction_factor

        self.x += self.vx * self.game.delta_time
        self.y += self.vy * self.game.delta_time

        if self.space:
            self.vx += self.speed
            self.space = False

        if self.x < -self.width:
            self.x = self.game.width
        if self.x > self.game.width:
            self.x = -self.width
        if self.y < -self.width:
            self.y = self.game.height
        if self.y > self.game.height:
            self.y = -self.width

        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = self.x + self.width / 2
        player_center_y = self.y + self.height / 2
        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        self.angle = math.degrees(math.atan2(dy, dx))