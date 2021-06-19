import pygame as py
import random
from game.game_logic.board import Board
from game.game_logic.game_objects.snake import Snake
from game.game_logic.game_objects.apple import Apple
from game.game_ai.snake_ai import SnakeAi


class Game:
    def __init__(self, width, caption, draw=True):
        py.init()
        self.WIDTH = width
        self.HEIGHT = width
        self.screen = py.display.set_mode((width, width))
        self.is_running = False
        self.is_game_running = False
        py.display.set_caption(caption)
        self.score = 0
        self.score_history = []
        self.drawing = draw
        # objects
        self.board = Board(width)
        self.snake = Snake(self.board.BOARD_SIZE // 2 - 1, self.board.BOARD_SIZE // 2 - 1, (0, 255, 0),
                           self.board.TILE_SIZE)
        self.apples = []
        self.generate_apples(1)
        # AI
        self.snake_ai = SnakeAi(self.board, self.snake, self.apples)

    def start(self):
        self.is_running = True
        self.is_game_running = True
        clock = py.time.Clock()
        self.snake_ai.update()
        while self.is_running:
            time_passed = clock.tick(999)
            # events, input
            self.handle_events()

            self.handle_input()

            if self.is_game_running:
                # update
                self.snake.update(time_passed)
                self.check_collision()
                if self.snake.moved and self.is_game_running:
                    self.snake_ai.update()
            else:
                break

            # draw
            if self.drawing:
                self.screen.fill((0, 0, 0))
                self.board.draw(self.screen)
                self.snake.draw(self.screen)
                for apple in self.apples:
                    apple.draw(self.screen)
                py.display.update()
        py.quit()
        return self.score

    def handle_events(self):
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                self.is_running = False

    def handle_input(self):
        keys_pressed = py.key.get_pressed()
        if keys_pressed[py.K_r]:
            self.restart_game()
        if keys_pressed[py.K_UP]:
            self.snake.change_direction((0, -1))
        elif keys_pressed[py.K_DOWN]:
            self.snake.change_direction((0, 1))
        elif keys_pressed[py.K_LEFT]:
            self.snake.change_direction((-1, 0))
        elif keys_pressed[py.K_RIGHT]:
            self.snake.change_direction((1, 0))

    def generate_apples(self, count):
        for i in range(count):
            x, y = self.get_new_random_position()
            self.apples.append(
                Apple(x, y, (255, 0, 0), 50))

    def get_new_random_position(self):
        snake_apple_tiles = set(self.snake.tail).union(set([(apple.rect.x, apple.rect.y) for apple in self.apples]))
        while True:
            x, y = random.randint(1, self.board.BOARD_SIZE - 2), random.randint(1, self.board.BOARD_SIZE - 2)
            if (x * 51, y * 51) not in snake_apple_tiles:
                return x, y

    def check_collision(self):
        apple_colliders = [apple.rect for apple in self.apples]
        collider_idx = self.snake.rect.collidelist(apple_colliders)
        if collider_idx != -1:
            self.snake.on_eat()
            x, y = self.get_new_random_position()
            self.apples[collider_idx].set_position(x, y)
            self.score += 1
            print("Score:", self.score)
            if self.score == (self.board.BOARD_SIZE - 2)**2 - 1:
                self.score += 1
                print("Score:", self.score)
                self.is_game_running = False

        snake_head_x, snake_head_y = self.snake.rect.x, self.snake.rect.y
        snake_tail_tiles = list(self.snake.tail)[:len(self.snake.tail) - 1]

        if self.board.board[snake_head_x // 51][snake_head_y // 51] == 0 or (
                snake_head_x, snake_head_y) in snake_tail_tiles:
            self.is_game_running = False
            self.score_history.append(self.score)
            print("Game ended.", "Score:", self.score, "/", (self.board.BOARD_SIZE - 2) ** 2)
            return

    def restart_game(self):
        self.is_game_running = True
        self.snake = Snake(self.board.BOARD_SIZE // 2 - 1, self.board.BOARD_SIZE // 2 - 1, (0, 255, 0), 50)
        self.score = 0
        self.snake_ai = SnakeAi(self.board, self.snake, self.apples)
        self.snake_ai.update()
