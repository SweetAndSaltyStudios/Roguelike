import constants
import helpers
import pygame

currently_selected_index = 0

def draw_debug(surface, debug_text, font):
    draw_text(surface, debug_text, (0, 0), font, constants.COLOR_WHITE, constants.COLOR_BLACK)


def draw_text(display_surface, text_to_display, coordinates, font, color = constants.COLOR_WHITE, background_color = None):

    text_surface, text_rect = helpers.helper_text_objects(
        text_to_display, 
        font,
        color, 
        background_color)

    text_rect = coordinates

    display_surface.blit(text_surface, text_rect)


# __  __ ___ _  _ _   _ ___ 
#|  \/  | __| \| | | | / __|
#| |\/| | _|| .` | |_| \__ \
#|_|  |_|___|_|\_|\___/|___/
          
                           
def show_menu_pause(surface, menu_text_font):
    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT
    menu_text = "PAUSED"

    text_height = helpers.helper_text_height(menu_text_font)
    text_width = helpers.helper_text_width(menu_text_font)
    text_coordinates = (window_width / 2) - (text_width / 2), (window_height / 2) - (text_height / 2)
    
    draw_text(
        surface,
        menu_text, 
        text_coordinates,
        menu_text_font,
        constants.COLOR_WHITE,
        constants.COLOR_BLACK)


def show_menu_inventory(surface, owner, menu_text_font, scroll_direction = 0):
    
    global currently_selected_index 

    currently_selected_index += scroll_direction

    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    menu_width = 200
    menu_height = 200
    menu_X = (window_width / 2) - (menu_width / 2)
    menu_Y = (window_height / 2) - (menu_height / 2)
    menu_coordinates = (menu_X, menu_Y)

    local_inventory_surface = pygame.Surface((menu_width, menu_height))
    local_inventory_surface.fill(constants.COLOR_BLACK)

    menu_text_horizontal_offset = 6
    menu_text_height = helpers.helper_text_height(menu_text_font)
    menu_text_color = constants.COLOR_WHITE

    item_list = [obj.name_object for obj in owner.container.inventory]

    if len(item_list) > 0:
        print(currently_selected_index)
        for item_index, (name) in enumerate(item_list):
            draw_text(
                local_inventory_surface,
                name, 
                (menu_text_horizontal_offset, 
                (item_index * menu_text_height)),
                menu_text_font,
                color = menu_text_color if currently_selected_index == item_index else constants.COLOR_RED)
    
    surface.blit(local_inventory_surface, menu_coordinates)
