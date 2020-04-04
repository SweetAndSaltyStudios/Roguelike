# 3rd party modules
import pygame

def game_handle_inputs(entity):

    event_list = pygame.event.get()

    for event in event_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if(event.type == pygame.KEYDOWN):

            if(event.key == pygame.K_UP):
                entity.creature.move(0, -1)
                return "player-moved"

            if(event.key == pygame.K_RIGHT):
                entity.creature.move(1, 0)
                return "player-moved"

            if(event.key == pygame.K_DOWN):
                entity.creature.move(0, 1)
                return "player-moved"

            if(event.key == pygame.K_LEFT):
                entity.creature.move(-1, 0)
                return "player-moved"

    return "no-action"