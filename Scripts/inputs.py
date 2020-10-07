# 3rd party modules
import pygame

def get_user_input():

    event_list = pygame.event.get()

    for event in event_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if(event.type == pygame.KEYUP):
            if event.key == pygame.K_p:
                return "PAUSED"
            elif(event.key == pygame.K_i):
                return "INVENTORY"

        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):
                return "UP"
            elif(event.key == pygame.K_RIGHT):
                return "RIGHT"
            elif(event.key == pygame.K_DOWN):
                return "DOWN"
            elif(event.key == pygame.K_LEFT):
                return "LEFT"
            elif(event.key == pygame.K_t):
                return "TAKE"  
            elif(event.key == pygame.K_d):
                return "DROP"
            elif(event.key == pygame.K_u):
                return "USE"

    return "NO-ACTION"