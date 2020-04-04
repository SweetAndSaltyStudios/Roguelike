#    _   ___
#   /_\ |_ _|
#  / _ \ | |
# /_/ \_\___|

# 3rd party modules
import tcod as libtcodpy
import pygame
import Main
import Constants

class Test:

    def take_turn(self):
        self.owner.creature.move(libtcodpy.random_get_int(0, -1, 1), libtcodpy.random_get_int(0, -1, 1))
    
def death_monster(monster):

    Main.draw_message(monster.creature.name + " is dead!", Constants.COLOR_RED)

    monster.creature = None
    monster.ai = None