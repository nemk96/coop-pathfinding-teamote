# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random
import numpy as np
import sys

from utils import *

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player

def main():

    init('carte_8')



    #-------------------------------
    # Building the matrix
    #-------------------------------


    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]


    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]

    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]



    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    start = initStates[0]
    pick = goalStates[0]
    center = (10,10)
    _wallStates = wall_to_matrix(wallStates)

    path_1, num_iter_1 = a_search(start,pick, _wallStates)
    path_2, num_iter_2 = a_search(pick,center, _wallStates)

    num_iter = num_iter_1 + num_iter_2
    length = len(path_1) + len(path_2)
    print('* Chemin : Start = {} --> Fiole = {} --> Centre = {}'.format(start,pick,center))
    print('* Total nombre d iterations a star : {}'.format(num_iter))
    print('* Longueur du chemin : {}'.format(length))

    #-------------------------------
    # Moving along the path
    #-------------------------------

    row,col = initStates[0]
    for pos in path_1:
        player.set_rowcol(*pos)
        game.mainiteration()
    game.player.ramasse(game.layers)
    for pos in path_2:
        player.set_rowcol(*pos)
        game.mainiteration()




    pygame.quit()





if __name__ == '__main__':
    main()
