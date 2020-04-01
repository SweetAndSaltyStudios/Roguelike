#  _____      _____ ___ _____     _   _  _ ___    ___   _   _  _______   __  ___ _____ _   _ ___ ___ ___  ___
# / __\ \    / / __| __|_   _|   /_\ | \| |   \  / __| /_\ | ||_   _\ \ / / / __|_   _| | | |   \_ _/ _ \/ __|
# \__ \\ \/\/ /| _|| _|  | |    / _ \| .` | |) | \__ \/ _ \| |__| |  \ V /  \__ \ | | | |_| | |) | | (_) \__ \
# |___/ \_/\_/ |___|___| |_|   /_/ \_\_|\_|___/  |___/_/ \_\____|_|   |_|   |___/ |_|  \___/|___/___\___/|___/

# 3rd party modules
import tcod as libtcodpy
import pygame

# game files
import Constants

#  ___ _____ ___ _   _  ___ _____ ___
# / __|_   _| _ \ | | |/ __|_   _/ __|
# \__ \ | | |   / |_| | (__  | | \__ \
# |___/ |_| |_|_\\___/ \___| |_| |___/


class struct_Tile:
    def __init__(self, isWalkable):
        self.isWalkable = isWalkable

#  ___ ___ _  _   ___   _____ ___  _   _ ___  ___
# | _ ) __| || | /_\ \ / /_ _/ _ \| | | | _ \/ __|
# | _ \ _|| __ |/ _ \ V / | | (_) | |_| |   /\__ \
# |___/___|_||_/_/ \_\_/ |___\___/ \___/|_|_\|___/


class obj_Monobehaviour:
    def __init__(self, x, y, name_object, sprite, creature = None):
        self.x = x
        self.y = y
        self.name_object = name_object
        self.sprite = sprite

        if creature:
            self.creature = creature
            creature.owner = self

    def draw(self):
        SURFACE_MAIN.blit(
            self.sprite, (self.x*Constants.CELL_WIDTH, self.y*Constants.CELL_HEIGHT))

    def move(self, delta_X, delta_Y):
        if WORLD_MAP[self.x + delta_X][self.y + delta_Y].isWalkable == True:
            self.x += delta_X
            self.y += delta_Y



#   ___ ___  __  __ ___  ___  _  _ ___ _  _ _____ ___ 
#  / __/ _ \|  \/  | _ \/ _ \| \| | __| \| |_   _/ __|
# | (_| (_) | |\/| |  _/ (_) | .` | _|| .` | | | \__ \
#  \___\___/|_|  |_|_|  \___/|_|\_|___|_|\_| |_| |___/

class com_Creature:

    def __init__(self, name_instnace, hp = 100):
        self.name:isinstance = name_instnace
        self.hp = hp


# class com_Item:

# class com_Container:
                                                  

#  __  __   _   ___
# |  \/  | /_\ | _ \
# | |\/| |/ _ \|  _/
# |_|  |_/_/ \_\_|


def map_create():
    new_map = [[struct_Tile(True) for y in range(0, Constants.MAP_WIDTH)]
               for x in range(0, Constants.MAP_WIDTH)]

    new_map[10][10].isWalkable = False
    new_map[10][15].isWalkable = False

    return new_map

#  ___ ___ _  _ ___  ___ ___ ___ _  _  ___
# | _ \ __| \| |   \| __| _ \_ _| \| |/ __|
# |   / _|| .` | |) | _||   /| || .` | (_ |
# |_|_\___|_|\_|___/|___|_|_\___|_|\_|\___|


def draw_game_canvas():

    global SURFACE_MAIN

    SURFACE_MAIN.fill(Constants.COLOR_DEFAULT_BACKGROUND)

    draw_map(WORLD_MAP)

    PLAYER.draw()

    ENEMY.draw()

    pygame.display.update()


def draw_map(map_to_draw):

    for x in range(0, Constants.MAP_WIDTH):
        for y in range(0, Constants.MAP_HEIGHT):
            if map_to_draw[x][y].isWalkable == True:
                SURFACE_MAIN.blit(
                    Constants.GROUND_SPRITE, (x*Constants.CELL_WIDTH, y*Constants.CELL_HEIGHT))
            else:
                SURFACE_MAIN.blit(
                    Constants.WALL_SPRITE, (x*Constants.CELL_WIDTH, y*Constants.CELL_HEIGHT))

#   ___   _   __  __ ___
#  / __| /_\ |  \/  | __|
# | (_ |/ _ \| |\/| | _|
#  \___/_/ \_\_|  |_|___|


def game_main_loop():

    game_quit = False

    while not game_quit:

        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                game_quit = True

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_UP):
                    PLAYER.move(0, -1)
                if(event.key == pygame.K_RIGHT):
                    PLAYER.move(1, 0)
                if(event.key == pygame.K_DOWN):
                    PLAYER.move(0, 1)
                if(event.key == pygame.K_LEFT):
                    PLAYER.move(-1, 0)

        draw_game_canvas()

    pygame.quit()
    exit()


def game_initialize():

    global SURFACE_MAIN
    global WORLD_MAP
    global PLAYER
    global ENEMY

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(
        (Constants.GAME_CANVAS_WIDTH, Constants.GAME_CANVAS_HEIGHT))

    WORLD_MAP = map_create()

    com_creature_1 = com_Creature("MAX")
    PLAYER = obj_Monobehaviour(0, 0, "HUMAN", Constants.PLAYER_SPRITE, creature = com_creature_1)

    com_creature_2 = com_Creature("SOLID")
    ENEMY = obj_Monobehaviour(4, 5, "SNAKE", Constants.ENEMY_SPRITE, creature = com_creature_2)


#  __  __   _   ___ _  _
# |  \/  | /_\ |_ _| \| |
# | |\/| |/ _ \ | || .` |
# |_|  |_/_/ \_\___|_|\_|


if __name__ == '__main__':
    game_initialize()
    game_main_loop()
