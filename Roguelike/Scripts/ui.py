import constants
import helpers
import pygame

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
          
                           
def menu_pause(surface, is_paused, menu_text_font):
    if is_paused:
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


def menu_inventory(surface, owner, in_inventory, menu_text_font):
    if in_inventory:

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

        print_list = [obj.name_object for obj in owner.container.inventory]

        ## Roguelike Tutorial - part 20 ->
        # mouse_X, mouse_Y = pygame.mouse.get_pos()

        # mouse_relative_X = mouse_X - menu_X
        # mouse_relative_Y = mouse_Y - menu_Y
        # mouse_in_window = (mouse_relative_X > 0 and
                            #  mouse_relative_Y > 0 and
                            #  mouse_relative_X < menu_width and
                            #  mouse_relative_XY < menu_height)
        
        # mouse_line_selection = mouse_relative_Y / menu_text_height
        # print(mouse_line_selection)

        for line, (name) in enumerate(print_list):
            
            # if line == mouse_line_selection and mouse_in_window:
            #     draw_text(
            #         local_inventory_surface,
            #         name, 
            #         (menu_text_horizontal_offset, 
            #         (line * menu_text_height)),
            #         menu_text_font,
            #         menu_text_color,
            #         constants.COLOR_RED)

            draw_text(
                local_inventory_surface,
                name, 
                (menu_text_horizontal_offset, 
                (line * menu_text_height)),
                menu_text_font,
                menu_text_color)

        surface.blit(local_inventory_surface, menu_coordinates)
