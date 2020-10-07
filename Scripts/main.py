import tcod as libtcodpy
import pygame

import constants


def game_main_loop():

    is_game_running = True

    while is_game_running == True:

        # TODO get player input

        # TODO process input

        # TODO draw the game
        print("Game is running!")

    # TODO quit the game


def game_initiailize():

    global CANVAS

    pygame.init()

    CANVAS = pygame.display.set_mode(
        (constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))


if __name__ == "__main__":

    game_initiailize()
    game_main_loop()
