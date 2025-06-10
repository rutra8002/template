import pygame
import math

class PhyObject:
    def __init__(self, game, width=50, height=50, x=0, y=0, speed=6000, friction=0.01):
        self.game = game
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = speed
        self.friction = friction
        self.angle = 0

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def apply_force(self, force_x, force_y):
        self.vx += force_x * self.game.delta_time
        self.vy += force_y * self.game.delta_time

    def apply_thrust(self, magnitude):
        angle_rad = math.radians(self.angle)
        self.vx += magnitude * math.cos(angle_rad)
        self.vy += magnitude * math.sin(angle_rad)

    def update_physics(self):
        friction_factor = self.friction ** self.game.delta_time
        self.vx *= friction_factor
        self.vy *= friction_factor

        self.x += self.vx * self.game.delta_time
        self.y += self.vy * self.game.delta_time

        self.wrap_position()

    def wrap_position(self):
        if self.x < -self.width:
            self.x = self.game.width
        if self.x > self.game.width:
            self.x = -self.width
        if self.y < -self.height:
            self.y = self.game.height
        if self.y > self.game.height:
            self.y = -self.height

    def render(self):
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
        rect = rotated_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        self.game.screen.blit(rotated_surface, rect.topleft)
