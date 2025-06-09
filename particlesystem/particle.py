import pygame

class Particle:
    def __init__(self, x: float, y: float, vx: float, vy: float, dvx: float, dvy: float, angle: float, dangle: float, speed: float, lifespan: int, size: int, red: int, green: int, blue: int, alpha: int, shape: str, gradient: bool = False) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dvx = dvx
        self.dvy = dvy
        self.angle = angle
        self.dangle = dangle
        self.speed = speed
        self.lifespan = lifespan
        self.size = size
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        self.shape = shape
        self.gradient = gradient
        self.mask_color = (255, 255, 255, 255)
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        surface.fill(self.mask_color)
        self.mask = pygame.mask.from_surface(surface)
        self.rect = pygame.Rect(self.x-self.size, self.y-self.size, self.size * 2, self.size * 2)

    def update_rect(self) -> None:
        self.rect = pygame.Rect(self.x-self.size, self.y-self.size, self.size * 2, self.size * 2)

    def apply_force(self, fx: float, fy: float) -> None:
        self.vx += fx
        self.vy += fy

    def update(self, x: float, y: float, delta_time: float = None) -> None:
        if delta_time is None:
            delta_time = 1.0
        self.apply_force(self.dvx * delta_time, self.dvy * delta_time)
        self.x += (self.vx * self.speed + x) * delta_time
        self.y += (self.vy * self.speed + y) * delta_time
        self.angle += self.dangle * delta_time
        if self.alpha > 0 and self.lifespan > 0:
            self.alpha -= self.alpha // (1 / 60 * self.lifespan) * delta_time
            self.lifespan -= 60 * delta_time
        self.update_rect()

    def draw(self, screen: pygame.Surface) -> None:
        # #draw mask
        #screen.blit(self.mask.to_surface(), self.rect.topleft)

        screen_width, screen_height = screen.get_size()
        if 0 <= self.x <= screen_width and 0 <= self.y <= screen_height:
            surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color = (self.red, self.green, self.blue, self.alpha)
            if self.gradient:
                for i in range(self.size, 0, -1):
                    gradient_color = (self.red, self.green, self.blue, self.alpha - int(self.alpha * (i / self.size)))
                    self.draw_shape(surface, gradient_color, i)
            else:
                self.draw_shape(surface, color, self.size)

            rotated_surface = pygame.transform.rotate(surface, self.angle)
            new_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_surface, new_rect.topleft)

    def draw_shape(self, surface: pygame.Surface, color: tuple, size: int) -> None:
        if self.shape == 'circle':
            pygame.draw.circle(surface, color, (self.size, self.size), size)
        elif self.shape == 'square':
            pygame.draw.rect(surface, color, pygame.Rect(self.size - size, self.size - size, size * 2, size * 2))
        elif self.shape == 'triangle':
            pygame.draw.polygon(surface, color, [(self.size, self.size - size), (self.size - size, self.size + size), (self.size + size, self.size + size)])
        elif self.shape == 'star':
            self.draw_star(surface, color, self.size, size)

    def draw_star(self, surface: pygame.Surface, color: tuple, size: int, i: int) -> None:
        points = [
            (size, size - i),
            (size + i * 0.2, size - i * 0.2),
            (size + i, size - i * 0.2),
            (size + i * 0.4, size + i * 0.2),
            (size + i * 0.6, size + i),
            (size, size + i * 0.4),
            (size - i * 0.6, size + i),
            (size - i * 0.4, size + i * 0.2),
            (size - i, size - i * 0.2),
            (size - i * 0.2, size - i * 0.2)
        ]
        pygame.draw.polygon(surface, color, points)

    def check_collision(self, other) -> bool:
        offset = (int(other.x - self.x), int(other.y - self.y))
        return self.mask.overlap(other.mask, offset) is not None