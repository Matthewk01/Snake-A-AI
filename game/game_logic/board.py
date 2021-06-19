import pygame as py


class Board:
    def __init__(self, size):
        self.TILE_SIZE = 50
        self.BOARD_SIZE = size // self.TILE_SIZE
        self.board = [[1] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE + 1)]
        self.make_borders()
        self.TILE_GAP = 1

    def draw(self, screen):
        surfFree = py.surface.Surface((self.TILE_SIZE, self.TILE_SIZE))
        surfFree.fill((0, 0, 0))
        surfBlocked = py.surface.Surface((self.TILE_SIZE, self.TILE_SIZE))
        surfBlocked.fill((255, 255, 255))
        for i, row in enumerate(self.board):
            for j, x in enumerate(row):
                if self.board[i][j] == 0:
                    screen.blit(surfFree, (j * (self.TILE_SIZE + self.TILE_GAP), i * (self.TILE_SIZE + self.TILE_GAP)))
                else:
                    screen.blit(surfBlocked,
                                (j * (self.TILE_SIZE + self.TILE_GAP), i * (self.TILE_SIZE + self.TILE_GAP)))

    def make_borders(self):
        for i in range(self.BOARD_SIZE):
            self.board[0][i] = 0
            self.board[self.BOARD_SIZE - 1][i] = 0
            self.board[i][0] = 0
            self.board[i][self.BOARD_SIZE - 1] = 0

    def is_position_valid(self, position):
        x, y = position
        if 0 <= x <= self.BOARD_SIZE - 1 and 0 <= y <= self.BOARD_SIZE - 1:
            return self.board[x][y] == 1
        return False
