from game.game_logic.game_objects.game_object import GameObject
from collections import deque


class Snake(GameObject):
    def __init__(self, x, y, color, width, height=0):
        super().__init__(x, y, color, width, height)
        self.max_size = 1
        self.current_size = 0
        self.tail = deque()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.tiles_per_second = 5000
        self.last_tick = 0
        self.moved = False

    def update(self, dt):
        if self.last_tick + dt > 1000 / self.tiles_per_second:
            self.direction = self.next_direction
            # check tail
            self.move()
            self.grow_tail_if_possible()
            self.last_tick = 0
            self.moved = True
        else:
            self.moved = False
        self.last_tick += dt

    def draw(self, surface):
        for tile in self.tail:
            surface.blit(self.surface, (tile[0], tile[1]))

    def grow_tail_if_possible(self):
        if self.current_size != self.max_size:
            self.tail.append((self.rect.x, self.rect.y))
            self.current_size += 1
        else:
            self.tail.append((self.rect.x, self.rect.y))
            self.tail.popleft()

    def move(self):
        self.rect.move_ip((self.direction[0] * 51, self.direction[1] * 51))

    def change_direction(self, direction):
        # if (self.direction == (1, 0) and direction == (-1, 0)) or (
        #         self.direction == (0, 1) and direction == (0, -1)) or (
        #         self.direction == (-1, 0) and direction == (1, 0)) or (
        #         self.direction == (0, -1) and direction == (0, 1)):
        #     return
        self.next_direction = direction

    def on_eat(self):
        self.max_size += 1
