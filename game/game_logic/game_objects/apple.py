from game.game_logic.game_objects.game_object import GameObject


class Apple(GameObject):
    def __init__(self, x, y, color, width, height=0):
        super().__init__(x, y, color, width, height)

    def set_position(self, x, y):
        self.rect.x, self.rect.y = x * 51, y * 51
