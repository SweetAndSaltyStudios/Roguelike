# 3rd party modules
import tcod as libtcodpy
import pygame

pygame.init()

# GAME CANVAS
GAME_CANVAS_WIDTH = 800
GAME_CANVAS_HEIGHT = 600
CELL_WIDTH = 16
CELL_HEIGHT = 16

# FPS
FPS_LIMIT = 30

# MAP VARIABLES 
MAP_WIDTH = 30
MAP_HEIGHT = 30

# COLORS
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)

COLOR_DEFAULT_BACKGROUND = COLOR_GREY

# SPRITES
PLAYER_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\player.png')
ENEMY_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\snake.png')

GROUND_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\ground.png')
GROUND_EXPLORED_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\ground_transparency.png')

WALL_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\wall.png')
WALL_EXPLORED_SPRITE = pygame.image.load('E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\wall_transparency.png')

# FIELD OF VIEW
FIELD_OF_VIEW_RADIUS = 10
FIELD_OF_VIEW_LIGHT_WALLS = True
FIELD_OF_VIEW_ALGORITHM = libtcodpy.FOV_BASIC

# FONTS
DEFAULT_FONT = pygame.font.Font(None, 22)
PIXEL_FONT = pygame.font.Font('E:\Python\Projects\Roguelike\Roguelike\Resources\Fonts\Pixeled.ttf', 12)

# MESSAGES
NUM_MESSAGES = 4