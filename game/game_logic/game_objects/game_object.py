import pygame as py


class GameObject:
    def __init__(self, x, y, color, width, height=0):
        height = height if height != 0 else width
        self.surface = py.surface.Surface((width, height))
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.rect.move_ip(x * 51, y * 51)

    def draw(self, surface):
        surface.blit(self.surface, (self.rect.x, self.rect.y))

    def update(self, dt):
        pass
