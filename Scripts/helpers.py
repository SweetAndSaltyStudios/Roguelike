#  _  _ ___ _    ___ ___ ___  ___
# | || | __| |  | _ \ __| _ \/ __|
# | __ | _|| |__|  _/ _||   /\__ \
# |_||_|___|____|_| |___|_|_\|___/


def helper_text_objects(text, font, color, background_color):
    if background_color:
        text_surface = font.render(text, False, color, background_color)
    else:
        text_surface = font.render(text, False, color)

    return text_surface, text_surface.get_rect()


def helper_text_height(font):
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height


def helper_text_width(font):
    font_object = font.render('a', False, (0,0,0))
    font_rect = font_object.get_rect()
    return font_rect.width
