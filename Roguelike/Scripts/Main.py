#  _____      _____ ___ _____     _   _  _ ___    ___   _   _  _______   __  ___ _____ _   _ ___ ___ ___  ___
# / __\ \    / / __| __|_   _|   /_\ | \| |   \  / __| /_\ | ||_   _\ \ / / / __|_   _| | | |   \_ _/ _ \/ __|
# \__ \\ \/\/ /| _|| _|  | |    / _ \| .` | |) | \__ \/ _ \| |__| |  \ V /  \__ \ | | | |_| | |) | | (_) \__ \
# |___/ \_/\_/ |___|___| |_|   /_/ \_\_|\_|___/  |___/_/ \_\____|_|   |_|   |___/ |_|  \___/|___/___\___/|___/

## TUTORIAL - PART 21 -USING ITEMS 23:37 ->
## USING ITEM FUNCTION DOES NOT WORK!

# 3rd party modules
import tcod as libtcodpy
import pygame

# game files
import constants
import inputs
import helpers
import ui

#  ___ _____ ___ _   _  ___ _____ ___
# / __|_   _| _ \ | | |/ __|_   _/ __|
# \__ \ | | |   / |_| | (__  | | \__ \
# |___/ |_| |_|_\\___/ \___| |_| |___/


class struct_Tile:

    def __init__(self, isWalkable):
        self.isWalkable = isWalkable
        self.isExplored = False


class struct_Assets:

    def __init__(self):

        self.player_sprite_sheet = obj_Sprite_sheet(
            "E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\characters.png")

        self.enemy_sprite_sheet = obj_Sprite_sheet(
            "E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\characters.png")

        self.PLAYER_ANIMATION = self.player_sprite_sheet.get_animation(
            'j', 1, 8, 8, 2, (16, 16))
        self.ENEMY_ANIMATION = self.enemy_sprite_sheet.get_animation(
            'f', 3, 8, 8, 2, (16, 16))

        self.GROUND_SPRITE = pygame.image.load(
            'E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\Ground.png')
        self.WALL_SPRITE = pygame.image.load(
            'E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\Wall.png')

        self.GROUND_EXPLORED_SPRITE = pygame.image.load(
            'E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\Tile_explored.png')
        self.WALL_EXPLORED_SPRITE = pygame.image.load(
            'E:\Python\Projects\Roguelike\Roguelike\Resources\Sprites\Tile_unexplored.png')

        # FONTS
        self.DEFAULT_FONT = pygame.font.Font(None, 22)
        self.PIXEL_FONT = pygame.font.Font(
            'E:\Python\Projects\Roguelike\Roguelike\Resources\Fonts\Pixeled.ttf', 12)


#   ___  ___    _ ___ ___ _____ ___
#  / _ \| _ )_ | | __/ __|_   _/ __|
# | (_) | _ \ || | _| (__  | | \__ \
#  \___/|___/\__/|___\___| |_| |___/


class obj_Entity:

    def __init__(
            self,
            x,
            y,
            name_object,
            animation,
            creature=None,
            ai=None,
            container=None,
            item=None):

        self.x = x
        self.y = y
        self.name_object = name_object
        self.animation = animation
        self.animation_speed = 0.5

        self.animation_rate = self.animation_speed / len(self.animation)
        self.animation_timer = 0.0
        self.current_sprite_index = 0

        self.creature = creature
        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

    def draw(self):
        is_visible = libtcodpy.map_is_in_fov(FIELD_OF_VIEW_MAP, self.x, self.y)

        if is_visible:
            if len(self.animation) == 1:
                SURFACE_MAIN.blit(
                    self.animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

            elif len(self.animation) > 1:

                if CLOCK.get_fps() > 0.0:
                    self.animation_timer += 1 / CLOCK.get_fps()

                if self.animation_timer >= self.animation_rate:
                    self.animation_timer = 0.0

                    if self.current_sprite_index >= len(self.animation) - 1:
                        self.current_sprite_index = 0

                    else:
                        self.current_sprite_index += 1

                SURFACE_MAIN.blit(self.animation[self.current_sprite_index], (
                    self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))


class obj_Game:
    def __init__(self):
        self.curret_map = map_create()
        self.current_game_objects = []
        self.game_message_history = []


class obj_Sprite_sheet:
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        self.tile_dictionary = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
                                'e': 5, 'f': 6, 'g': 7, 'h': 8,
                                'i': 9, 'j': 10, 'k': 11, 'l': 12,
                                'm': 13, 'n': 14, 'o': 15, 'p': 16}

    def get_sprite(self, column, row,
                   width=constants.CELL_WIDTH,
                   height=constants.CELL_HEIGHT,
                   scale=None):

        sprite_list = []

        sprite = pygame.Surface([width, height]).convert()

        sprite.blit(self.sprite_sheet, (0, 0),
                    (self.tile_dictionary[column] * width, row * height, width, height))

        if scale:
            (new_width, new_height) = scale
            sprite = pygame.transform.scale(sprite, (new_width, new_height))

        sprite_list.append(sprite)

        return sprite_list

    def get_animation(self, column, row,
                      width=constants.CELL_WIDTH,
                      height=constants.CELL_HEIGHT,
                      animation_lenght=1,
                      scale=None):

        sprite_list = []

        for i in range(animation_lenght):

            sprite = pygame.Surface([width, height]).convert()

            sprite.blit(self.sprite_sheet, (0, 0), (
                self.tile_dictionary[column] * width + (width * i), row * height, width, height))

            sprite.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_width, new_height) = scale
                sprite = pygame.transform.scale(
                    sprite, (new_width, new_height))

            sprite_list.append(sprite)

        return sprite_list


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

        message = self.name + "'s health is " + \
            str(self.hp) + "/" + str(self.max_hp)
        game_message(message, constants.COLOR_WHITE)

        if self.hp <= 0:
            if self.on_death is not None:
                self.on_death(self.owner)

    def move(self, delta_X, delta_Y):

        target_tile = (GAME.curret_map[self.owner.x + delta_X]
                       [self.owner.y + delta_Y])

        target = map_check_for_creatures(
            self.owner.x + delta_X, self.owner.y + delta_Y, self.owner)

        if target:
            self.attack(target, -70)

        if target_tile.isWalkable and target is None:
            self.owner.x += delta_X
            self.owner.y += delta_Y

    def attack(self, target, damage):
        game_message((self.name + " attacks " + target.creature.name +
                      " for 60 damage!"), constants.COLOR_WHITE)
        target.creature.modify_hp(damage)


class com_container:
    def __init__(self, volume=10.0, inventory=None):

        self.max_volume = volume

        if inventory is None:
            self.inventory = []
        else:
            self.inventory = inventory

    # TODO Get names of everything in inventory

    # TODO Get volume within container
    @property
    def volume(self):
        return 0.0

    # TODO Get weight of everything in inventory


class com_item:

    def __init__(self, weight=0.0, volume=0.0, use_function=None, value=None):
        self.value = value
        self.weight = weight
        self.use_function = use_function
        self.volume = volume

    def take(self, entity):
        if entity.container:
            if entity.container.volume + self.volume > entity.container.max_volume:
                game_message("Not enought room to pick up")
            else:
                entity.container.inventory.append(self.owner)
                game_message("Picking up")
                GAME.current_game_objects.remove(self.owner)
                self.container = entity.container

    def drop(self, x, y):
        GAME.current_game_objects.append(self.owner)
        self.container.inventory.remove(self.owner)
        self.owner.x = x
        self.owner.y = y
        game_message("Item dropped!")

    def use(self):
        if self.use_function:
            result = self.use_function(self.owner.container.owner, self.value)

            if result is not None:
                print("Use function failed")
            else:
                self.container.inventory.remove(self.owner)

#    _   ___
#   /_\ |_ _|
#  / _ \ | |
# /_/ \_\___|


class ai_test:

    def process_turn(self):
        self.owner.creature.move(libtcodpy.random_get_int(
            0, -1, 1), libtcodpy.random_get_int(0, -1, 1))


def death_monster(monster):

    game_message(monster.creature.name + " is dead!", constants.COLOR_RED)

    monster.creature = None
    monster.ai = None

#  __  __   _   ___
# |  \/  | /_\ | _ \
# | |\/| |/ _ \|  _/
# |_|  |_/_/ \_\_|


def map_create():

    new_map = [[struct_Tile(True) for y in range(0, constants.MAP_WIDTH)]
               for x in range(0, constants.MAP_WIDTH
                              )]

    new_map[10][10].isWalkable = False
    new_map[10][15].isWalkable = False

    for x in range(constants.MAP_WIDTH):
        new_map[x][0].isWalkable = False
        new_map[x][constants.MAP_HEIGHT - 1].isWalkable = False

    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].isWalkable = False
        new_map[constants.MAP_WIDTH - 1][y].isWalkable = False

    map_make_field_of_view(new_map)

    return new_map


def map_check_for_creatures(x, y, exclude_object=None):

    target = None

    if exclude_object:
        for object in GAME.current_game_objects:
            if(object is not exclude_object and
               object.x == x and
               object.y == y and
               object.creature):
                target = object

            if target:
                return target
    else:
        for object in GAME.current_game_objects:
            if(object.x == x and
               object.y == y and
               object.creature):
                target = object

            if target:
                return target


def map_make_field_of_view(map):
    global FIELD_OF_VIEW_MAP

    FIELD_OF_VIEW_MAP = libtcodpy.map.Map(
        constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
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
            constants.FIELD_OF_VIEW_RADIUS,
            constants.FIELD_OF_VIEW_LIGHT_WALLS,
            constants.FIELD_OF_VIEW_ALGORITHM)


def map_objects_at_coordinates(x, y):

    object_options = [obj for obj in GAME.current_game_objects
                      if obj.x == x and obj.y == y]

    return object_options

#  ___ ___ _  _ ___  ___ ___ ___ _  _  ___
# | _ \ __| \| |   \| __| _ \_ _| \| |/ __|
# |   / _|| .` | |) | _||   /| || .` | (_ |
# |_|_\___|_|\_|___/|___|_|_\___|_|\_|\___|


def draw_game_canvas():
    global SURFACE_MAIN
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BACKGROUND)
    draw_map(GAME.curret_map)

    for obj in GAME.current_game_objects:
        obj.draw()

    ui.draw_debug(
        SURFACE_MAIN,
        "FOO",
        ASSETS.DEFAULT_FONT)

    draw_message()
    pygame.display.update()


def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            isVisible = libtcodpy.map_is_in_fov(FIELD_OF_VIEW_MAP, x, y)

            if isVisible:

                map_to_draw[x][y].isExplored = True

                if map_to_draw[x][y].isWalkable == True:
                    SURFACE_MAIN.blit(
                        ASSETS.GROUND_SPRITE, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(
                        ASSETS.WALL_SPRITE, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
            else:

                if map_to_draw[x][y].isExplored == True:
                    SURFACE_MAIN.blit(
                        ASSETS.GROUND_EXPLORED_SPRITE, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(
                        ASSETS.WALL_EXPLORED_SPRITE, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))


def draw_message():
    if len(GAME.game_message_history) <= constants.NUM_MESSAGES:
        messages_to_draw = GAME.game_message_history
    else:
        messages_to_draw = GAME.game_message_history[-(
            constants.NUM_MESSAGES):]

    text_height = helpers.helper_text_height(ASSETS.PIXEL_FONT)

    start_Y = constants.MAP_HEIGHT * constants.CELL_HEIGHT - \
        (constants.NUM_MESSAGES * text_height)

    i = 0

    for message, color in messages_to_draw:
        ui.draw_text(
            SURFACE_MAIN, message,
            (0, start_Y + (i * text_height)),
            ASSETS.DEFAULT_FONT,
            color,
            constants.COLOR_BLACK)

        i += 1


# ___ ___ ___ ___ ___ _____ ___
# | __| __| __| __/ __|_   _/ __|
# | _|| _|| _|| _| (__  | | \__ \
# |___|_| |_| |___\___| |_| |___/

def cast_heal(target, value):
    print("Target: " + target.name + "heald for  " + str(value))

    return None


#   ___   _   __  __ ___
#  / __| /_\ |  \/  | __|
# | (_ |/ _ \| |\/| | _|
#  \___/_/ \_\_|  |_|___|


def game_main_loop():

    game_is_Running = True
    game_action_preformed = False
    player_action_preformed = False
    user_action = "no-action"

    while game_is_Running:

        user_action = inputs.get_user_input()
        game_action_preformed = game_actions(user_action)

        if game_action_preformed:
            continue

        if IS_PAUSED or IN_INVENTORY:
            CLOCK.tick(constants.FPS_LIMIT)
            continue

        player_action_preformed = player_actions(user_action)

        if user_action != "no-action":
            for obj in GAME.current_game_objects:
                if obj.ai:
                    obj.ai.process_turn()

        draw_game_canvas()
        CLOCK.tick(constants.FPS_LIMIT)

    pygame.quit()
    exit()


def game_actions(user_action):
    global IS_PAUSED
    global IN_INVENTORY

    if user_action == "QUIT":
        game_is_Running = False
    elif user_action == "PAUSED":
        IS_PAUSED = not IS_PAUSED
        ui.menu_pause(SURFACE_MAIN, IS_PAUSED, ASSETS.DEFAULT_FONT)
        pygame.display.update()
        return True
    elif user_action == "INVENTORY":
        IN_INVENTORY = not IN_INVENTORY
        ui.menu_inventory(SURFACE_MAIN, PLAYER,
                          IN_INVENTORY, ASSETS.PIXEL_FONT)
        pygame.display.update()
        return True


def player_actions(user_action):
    global FIELD_OF_VIEW_CALCULATE

    map_calculate_field_of_view()

    if user_action == "UP":
        PLAYER.creature.move(0, -1)
        FIELD_OF_VIEW_CALCULATE = True
        return True
    elif user_action == "LEFT":
        PLAYER.creature.move(-1, 0)
        FIELD_OF_VIEW_CALCULATE = True
        return True
    elif user_action == "DOWN":
        PLAYER.creature.move(0, 1)
        FIELD_OF_VIEW_CALCULATE = True
        return True
    elif user_action == "RIGHT":
        PLAYER.creature.move(1, 0)
        FIELD_OF_VIEW_CALCULATE = True
        return True
    elif user_action == "TAKE":
        objects_at_player = map_objects_at_coordinates(PLAYER.x, PLAYER.y)
        for obj in objects_at_player:
            if obj.item:
                obj.item.take(PLAYER)
        return True
    elif user_action == "DROP":
        if len(PLAYER.container.inventory) > 0:
            last_item_in_inventory = PLAYER.container.inventory[-1].item
            if last_item_in_inventory:
                last_item_in_inventory.drop(PLAYER.x, PLAYER.y)
                return True
    elif user_action == "USE":
        if len(PLAYER.container.inventory) > 0:
            last_item_in_inventory = PLAYER.container.inventory[-1].item
            if last_item_in_inventory:
                last_item_in_inventory.use_function()
                return True

    return False


def game_message(message, color=constants.COLOR_WHITE):

    GAME.game_message_history.append((message, color))


def game_initialize():

    global SURFACE_MAIN
    global GAME
    global CLOCK
    global FIELD_OF_VIEW_CALCULATE
    global PLAYER
    global ENEMY
    global ASSETS
    global IS_PAUSED
    global IN_INVENTORY

    pygame.init()

    press_delay = 200
    press_interval = 70
    pygame.key.set_repeat(press_delay, press_interval)

    SURFACE_MAIN = pygame.display.set_mode(
        (constants.MAP_WIDTH * constants.CELL_WIDTH,
         constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    GAME = obj_Game()

    CLOCK = pygame.time.Clock()

    FIELD_OF_VIEW_CALCULATE = True

    ASSETS = struct_Assets()

    IS_PAUSED = False
    IN_INVENTORY = False

    com_container_1 = com_container()
    com_creature_1 = com_creature("MAX")

    PLAYER = obj_Entity(
        2, 2, "HUMAN", ASSETS.PLAYER_ANIMATION,
        creature=com_creature_1,
        container=com_container_1)

    com_item_1 = com_item(value=4, use_function=cast_heal)
    com_creature_2 = com_creature("SOLID", on_death=death_monster)
    com_ai_1 = ai_test()
    ENEMY = obj_Entity(
        15, 10, "SNAKE 1", ASSETS.ENEMY_ANIMATION,
        creature=com_creature_2,
        ai=com_ai_1,
        item=com_item_1)

    com_item_2 = com_item(value=4, use_function=cast_heal)
    com_creature_3 = com_creature("DUMB", on_death=death_monster)
    ENEMY_2 = obj_Entity(
        14, 10, "SNAKE 2", ASSETS.ENEMY_ANIMATION,
        creature=com_creature_3,
        item=com_item_2)

    GAME.current_game_objects = [PLAYER, ENEMY, ENEMY_2]

#  __  __   _   ___ _  _
# |  \/  | /_\ |_ _| \| |
# | |\/| |/ _ \ | || .` |
# |_|  |_/_/ \_\___|_|\_|


if __name__ == '__main__':
    game_initialize()
    game_main_loop()
