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
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

def main():


    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    init('carte_5')





    #-------------------------------
    # Initialisation
    #-------------------------------

    players = [o for o in game.layers['joueur']]




    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in players]
    print ("Init states:", initStates)


    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']][::-1]
    print ("Goal states:", goalStates)

    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)


    nbPlayers = min(len(players), len(goalStates))
    score = [0]*nbPlayers
    #-------------------------------
    # Placement aleatoire des fioles
    #-------------------------------

    # Initialize paths

    paths = nbPlayers*[None]
    walls = []
    timetable = []
    num_iter = 0
    types_order = ['random', 'far', 'close']
    type_order = types_order[2]
    if type_order == 'random':
        order = list(range(nbPlayers))
        random.shuffle(order)
    else:
        order = list(range(nbPlayers))
        distances = list(map(lambda idx: manhattan(initStates[idx], goalStates[idx]), order))
        if type_order == 'far':
            order = sorted(order, key=lambda idx: distances[idx])
        elif type_order == 'close':
            order = sorted(order, key=lambda idx: distances[idx])[::-1]

    for j in order:
        start = initStates[j][0], initStates[j][1], 0
        destination = goalStates[j][0], goalStates[j][1], None
        path, timetable, a, _ = a_search_bis(start,destination, wallStates,timetable)
        num_iter += a
        paths[j] = path

        print('Player {} done'.format(j))

    t_max = max(list(map(len,paths)))
    for j in range(nbPlayers):
        if len(paths[j]) < t_max:
            paths[j] += (t_max-len(paths[j]))*[goalStates[j]]
    #all_moves = list(map(list,map(None,*paths)))
    all_moves = [list(i) for i in zip(*paths)]


    posPlayers = initStates
    picked = nbPlayers*[False]
    for moves in all_moves:
        for j in range(nbPlayers):
            players[j].set_rowcol(*moves[j][:2])
            if (not picked[j]):
                score[j] += 1
                if (moves[j][:2] == goalStates[j]):
                    players[j].ramasse(game.layers)
                    picked[j] = True

        game.mainiteration()
    print ("scores:", score)
    print('total score', max(score))
    print('num_iter', num_iter)
    pygame.quit()





if __name__ == '__main__':
    main()
