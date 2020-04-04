#  _____      _____ ___ _____     _   _  _ ___    ___   _   _  _______   __  ___ _____ _   _ ___ ___ ___  ___
# / __\ \    / / __| __|_   _|   /_\ | \| |   \  / __| /_\ | ||_   _\ \ / / / __|_   _| | | |   \_ _/ _ \/ __|
# \__ \\ \/\/ /| _|| _|  | |    / _ \| .` | |) | \__ \/ _ \| |__| |  \ V /  \__ \ | | | |_| | |) | | (_) \__ \
# |___/ \_/\_/ |___|___| |_|   /_/ \_\_|\_|___/  |___/_/ \_\____|_|   |_|   |___/ |_|  \___/|___/___\___/|___/

# 3rd party modules
import tcod as libtcodpy
import pygame

# game files
import Constants
import Inputs
import AI

#  ___ _____ ___ _   _  ___ _____ ___
# / __|_   _| _ \ | | |/ __|_   _/ __|
# \__ \ | | |   / |_| | (__  | | \__ \
# |___/ |_| |_|_\\___/ \___| |_| |___/


class struct_Tile:

    def __init__(self, isWalkable):
        self.isWalkable = isWalkable
        self.isExplored = False

#   ___  ___    _ ___ ___ _____ ___
#  / _ \| _ )_ | | __/ __|_   _/ __|
# | (_) | _ \ || | _| (__  | | \__ \
#  \___/|___/\__/|___\___| |_| |___/


class obj_Entity:

    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x
        self.y = y
        self.name_object = name_object
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):

        isVisible = libtcodpy.map_is_in_fov(FIELD_OF_VIEW_MAP, self.x, self.y)

        if isVisible:
            SURFACE_MAIN.blit(
                self.sprite, (self.x*Constants.CELL_WIDTH, self.y*Constants.CELL_HEIGHT))


#   ___ ___  __  __ ___  ___  _  _ ___ _  _ _____ ___
#  / __/ _ \|  \/  | _ \/ _ \| \| | __| \| |_   _/ __|
# | (_| (_) | |\/| |  _/ (_) | .` | _|| .` | | | \__ \
#  \___\___/|_|  |_|_|  \___/|_|\_|___|_|\_| |_| |___/


class com_creature:

    def __init__(self, name_instnace, hp=100, on_death=None):
        self.name = name_instnace
        self.max_hp = hp
        self.hp = hp
        self.on_death = on_death

    def modify_hp(self, value):
        self.hp += value

        message = self.name + "'s health is " + str(self.hp) + "/" + str(self.max_hp)
        draw_message(message, Constants.COLOR_WHITE)

        if self.hp <= 0:
            if self.on_death is not None:
                self.on_death(self.owner)

    def move(self, delta_X, delta_Y):

        target_tile = (WORLD_MAP[self.owner.x + delta_X]
                       [self.owner.y + delta_Y])

        target = map_check_for_creatures(
            self.owner.x + delta_X, self.owner.y + delta_Y, self.owner)

        if target:
            self.attack(target, -70)

        if target_tile.isWalkable and target is None:
            self.owner.x += delta_X
            self.owner.y += delta_Y

    def attack(self, target, damage):
        game_message((self.name + " attacks " + target.creature.name + " for 60 damage!"), Constants.COLOR_WHITE)
        target.creature.modify_hp(damage)

#  __  __   _   ___
# |  \/  | /_\ | _ \
# | |\/| |/ _ \|  _/
# |_|  |_/_/ \_\_|


def map_create():

    new_map = [[struct_Tile(True) for y in range(0, Constants.MAP_WIDTH)]
               for x in range(0, Constants.MAP_WIDTH
                              )]

    new_map[10][10].isWalkable = False
    new_map[10][15].isWalkable = False

    for x in range(Constants.MAP_WIDTH):
        new_map[x][0].isWalkable = False
        new_map[x][Constants.MAP_HEIGHT - 1].isWalkable = False

    for y in range(Constants.MAP_HEIGHT):
        new_map[0][y].isWalkable = False
        new_map[Constants.MAP_WIDTH - 1][y].isWalkable = False

    map_make_field_of_view(new_map)

    return new_map


def map_check_for_creatures(x, y, exclude_object=None):

    target = None

    if exclude_object:
        for object in GAME_OBJECTS:
            if(object is not exclude_object and
               object.x == x and
               object.y == y and
               object.creature):
                target = object

            if target:
                return target
    else:
        for object in GAME_OBJECTS:
            if(object.x == x and
               object.y == y and
               object.creature):
                target = object

            if target:
                return target


def map_make_field_of_view(map):
    global FIELD_OF_VIEW_MAP

    FIELD_OF_VIEW_MAP = libtcodpy.map_new(
        Constants.MAP_WIDTH, Constants.MAP_HEIGHT)

    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            libtcodpy.map_set_properties(FIELD_OF_VIEW_MAP, x, y,
                                         map[x][y].isWalkable, map[x][y].isWalkable)


def map_calculate_field_of_view():

    global FIELD_OF_VIEW_CALCULATE

    if FIELD_OF_VIEW_CALCULATE:
        FIELD_OF_VIEW_CALCULATE = False

        libtcodpy.map_compute_fov(
            FIELD_OF_VIEW_MAP,
            PLAYER.x,
            PLAYER.y,
            Constants.FIELD_OF_VIEW_RADIUS,
            Constants.FIELD_OF_VIEW_LIGHT_WALLS,
            Constants.FIELD_OF_VIEW_ALGORITHM)


#  ___ ___ _  _ ___  ___ ___ ___ _  _  ___
# | _ \ __| \| |   \| __| _ \_ _| \| |/ __|
# |   / _|| .` | |) | _||   /| || .` | (_ |
# |_|_\___|_|\_|___/|___|_|_\___|_|\_|\___|


def draw_game_canvas():

    global SURFACE_MAIN

    SURFACE_MAIN.fill(Constants.COLOR_DEFAULT_BACKGROUND)

    draw_map(WORLD_MAP)

    for obj in GAME_OBJECTS:
        obj.draw()

    draw_debug()

    draw_message()

    pygame.display.update()


def draw_map(map_to_draw):

    for x in range(0, Constants.MAP_WIDTH):
        for y in range(0, Constants.MAP_HEIGHT):

            isVisible = libtcodpy.map_is_in_fov(FIELD_OF_VIEW_MAP, x, y)

            if isVisible:

                map_to_draw[x][y].isExplored = True

                if map_to_draw[x][y].isWalkable == True:
                    SURFACE_MAIN.blit(
                        Constants.GROUND_SPRITE, (x*Constants.CELL_WIDTH, y*Constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(
                        Constants.WALL_SPRITE, (x*Constants.CELL_WIDTH, y*Constants.CELL_HEIGHT))
            else:

                if map_to_draw[x][y].isExplored == True:
                    SURFACE_MAIN.blit(
                        Constants.GROUND_EXPLORED_SPRITE, (x*Constants.CELL_WIDTH, y*Constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(
                        Constants.WALL_EXPLORED_SPRITE, (x*Constants.CELL_WIDTH, y*Constants.CELL_HEIGHT))

def draw_debug():

    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())),
              (0, 0), Constants.COLOR_WHITE, Constants.COLOR_BLACK)

def draw_message():

    if len(GAME_MESSAGES) <= Constants.NUM_MESSAGES:
        messages_to_draw = GAME_MESSAGES
    else:
        messages_to_draw = GAME_MESSAGES(-Constants.NUM_MESSAGES)

    text_height = helper_text_height(Constants.PIXEL_FONT)

    start_Y = Constants.MAP_HEIGHT * Constants.CELL_HEIGHT - (Constants.NUM_MESSAGES * text_height)
    
    i = 0

    for message, color in messages_to_draw:

        draw_text(SURFACE_MAIN, message, (0, start_Y + (i * text_height)), color, Constants.COLOR_BLACK)

        i += 1

def draw_text(display_surface, text_to_display, coordinates, color, background_color=None):

    text_surface, text_rect = helper_text_objects(
        text_to_display, color, background_color)

    text_rect = coordinates

    display_surface.blit(text_surface, text_rect)


#  _  _ ___ _    ___ ___ ___  ___
# | || | __| |  | _ \ __| _ \/ __|
# | __ | _|| |__|  _/ _||   /\__ \
# |_||_|___|____|_| |___|_|_\|___/

def helper_text_objects(text, color, background_color):

    if background_color:
        text_surface = Constants.DEFAULT_FONT.render(
            text, False, color, background_color)
    else:
        text_surface = Constants.DEFAULT_FONT.render(text, False, color)

    return text_surface, text_surface.get_rect()

def helper_text_height(font):

    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height

#   ___   _   __  __ ___
#  / __| /_\ |  \/  | __|
# | (_ |/ _ \| |\/| | _|
#  \___/_/ \_\_|  |_|___|


def game_main_loop():

    global FIELD_OF_VIEW_CALCULATE

    game_is_Running = True

    player_action = "no-action"

    while game_is_Running:

        player_action = Inputs.game_handle_inputs(PLAYER)

        map_calculate_field_of_view()

        if player_action == "QUIT":
            game_is_Running = False

        if player_action == "player-moved":
            FIELD_OF_VIEW_CALCULATE = True

        if player_action != "no-action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        draw_game_canvas()

        CLOCK.tick(Constants.FPS_LIMIT)

    pygame.quit()
    exit()

def game_message(message, color):

    GAME_MESSAGES.append((message, color))

    print("Python Roguelike Tutorial - Part 12 - In Game Message Console -> 12:25 / 35:31 ")

def game_initialize():

    global SURFACE_MAIN
    global WORLD_MAP
    global PLAYER
    global ENEMY
    global GAME_OBJECTS
    global FIELD_OF_VIEW_CALCULATE
    global CLOCK
    global GAME_MESSAGES

    pygame.init()

    CLOCK = pygame.time.Clock()

    SURFACE_MAIN = pygame.display.set_mode(
        (Constants.MAP_WIDTH * Constants.CELL_WIDTH,
         Constants.MAP_HEIGHT * Constants.CELL_HEIGHT))

    WORLD_MAP = map_create()

    GAME_MESSAGES = []

    game_message("test message 1", Constants.COLOR_WHITE)
    game_message("test message 2", Constants.COLOR_WHITE)
    game_message("test message 3", Constants.COLOR_WHITE)
    game_message("test message 4", Constants.COLOR_RED)

    FIELD_OF_VIEW_CALCULATE = True

    com_creature_1 = com_creature("MAX")
    PLAYER = obj_Entity(
        2, 2, "HUMAN", Constants.PLAYER_SPRITE, creature=com_creature_1)

    com_creature_2 = com_creature("SOLID", on_death=AI.death_monster)
    com_ai_1 = AI.Test()
    ENEMY = obj_Entity(
        15, 10, "SNAKE", Constants.ENEMY_SPRITE, creature=com_creature_2, ai=com_ai_1)

    GAME_OBJECTS = [PLAYER, ENEMY]



    #  __  __   _   ___ _  _
    # |  \/  | /_\ |_ _| \| |
    # | |\/| |/ _ \ | || .` |
    # |_|  |_/_/ \_\___|_|\_|


if __name__ == '__main__':
    game_initialize()
    game_main_loop()
