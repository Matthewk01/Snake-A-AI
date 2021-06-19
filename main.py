import pygame
from game.game_logic.game import Game
import matplotlib.pyplot as plt


def main():
    scores_history = []
    GAME_COUNT = 2
    for i in range(GAME_COUNT):
        game = Game(400, "Snake AI")
        score = game.start()
        scores_history.append(score)
        print("Game:", i)

    plt.ylim(0, 36)
    plt.plot(range(len(scores_history)), scores_history)
    plt.ylabel('Snake length')
    plt.xlabel('Game count')
    plt.show()


if __name__ == "__main__":
    main()
