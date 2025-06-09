import pygame

class ParticleGenerator:
    def __init__(self, particle_system, x: float, y: float, vx: float, vy: float, dvx: float, dvy: float, angle: float, dangle: float, speed: float, lifespan: int, size: int, red: int, green: int, blue: int, alpha: int, shape: str, gradient: bool, rate: float) -> None:
        self.particle_system = particle_system
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
        self.rate = rate
        self.time_since_last_particle = 0.0
        self.active = False

    def start(self) -> None:
        self.active = True

    def stop(self) -> None:
        self.active = False

    def update(self, delta_time: float) -> None:
        if not self.active:
            return
        self.time_since_last_particle += delta_time
        while self.time_since_last_particle >= 1.0 / self.rate:
            self.particle_system.add_particle(self.x, self.y, self.vx, self.vy, self.dvx, self.dvy, self.angle, self.dangle, self.speed, self.lifespan, self.size, self.red, self.green, self.blue, self.alpha, self.shape, self.gradient)
            self.time_since_last_particle -= 1.0 / self.rate

    def edit(self, x: float = None, y: float = None, vx: float = None, vy: float = None, dvx: float = None, dvy: float = None, angle: float = None, dangle: float = None, speed: float = None, lifespan: int = None, size: int = None, red: int = None, green: int = None, blue: int = None, alpha: int = None, shape: str = None, gradient: bool = None, rate: float = None) -> None:
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if vx is not None:
            self.vx = vx
        if vy is not None:
            self.vy = vy
        if dvx is not None:
            self.dvx = dvx
        if dvy is not None:
            self.dvy = dvy
        if angle is not None:
            self.angle = angle
        if dangle is not None:
            self.dangle = dangle
        if speed is not None:
            self.speed = speed
        if lifespan is not None:
            self.lifespan = lifespan
        if size is not None:
            self.size = size
        if red is not None:
            self.red = red
        if green is not None:
            self.green = green
        if blue is not None:
            self.blue = blue
        if alpha is not None:
            self.alpha = alpha
        if shape is not None:
            self.shape = shape
        if gradient is not None:
            self.gradient = gradient
        if rate is not None:
            self.rate = rate