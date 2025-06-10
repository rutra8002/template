import pygame
import math
from app.object import PhyObject


class Player(PhyObject):
    def __init__(self, game):
        super().__init__(game, width=50, height=50, speed=6000, friction=0.01)
        self.w = self.a = self.d = self.s = self.space = False

        pygame.draw.rect(self.surface, (255, 0, 0), (0, 0, self.width, self.height))

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
        self.apply_movement_forces()
        super().update_physics()
        self.apply_movement_forces()
        self.set_mouse_angle()

    def apply_movement_forces(self):
        if self.w:
            self.apply_force(0, -self.speed / 2)
        if self.s:
            self.apply_force(0, self.speed / 2)
        if self.a:
            self.apply_force(-self.speed / 2, 0)
        if self.d:
            self.apply_force(self.speed / 2, 0)

        if self.space:
            self.apply_thrust(self.speed / 2)
            self.space = False

    def set_mouse_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = self.x + self.width / 2
        player_center_y = self.y + self.height / 2
        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        self.angle = math.degrees(math.atan2(dy, dx))