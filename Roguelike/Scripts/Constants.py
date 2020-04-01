import pygame

pygame.init()

# GAME CANVAS
GAME_CANVAS_WIDTH = 800
GAME_CANVAS_HEIGHT = 600
CELL_WIDTH = 8
CELL_HEIGHT = 8

# MAP VARIABLES 
MAP_WIDTH = 30
MAP_HEIGHT = 30

# COLORS
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

COLOR_DEFAULT_BACKGROUND = COLOR_GREY

# SPRITES
PLAYER_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\player.png')
ENEMY_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\snake.png')
GROUND_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\ground.png')
WALL_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\wall.png')