# 3rd party modules
import tcod as libtcodpy
import pygame

# game files
import Constants


def draw_game():

    global SURFACE_MAIN

    SURFACE_MAIN.fill(Constants.COLOR_DEFAULT_BACKGROUND)

    SURFACE_MAIN.blit(Constants.PLAYER_SPRITE, (50, 20))


def game_main_loop():

    game_quit = False

    while not game_quit:

        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                game_quit = True

        draw_game()

    pygame.quit()
    exit()


def game_initialize():

    global SURFACE_MAIN

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((Constants.GAME_WIDTH, Constants.GAME_HEIGHT))


if __name__ == '__main__':
    game_initialize()
    game_main_loop()
