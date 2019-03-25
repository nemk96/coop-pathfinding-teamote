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
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    # goalStates  = goalStates[::-1]
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
    num_iter = 0
    length = 0

    paths = []
    walls = []
    for j in range(nbPlayers):
        obstacles = wallStates + [goalStates[k] for k in range(nbPlayers) if k!=j ]
        walls.append(obstacles)
        path, a = a_search(initStates[j],goalStates[j], obstacles)
        num_iter += a
        paths.append(path)
    reached = nbPlayers * [False]
    borne_inf = max(list(map(len, paths)))

    actual_moves = [path[0] for path in paths]
    all_moves = [actual_moves]


    types_order = ['random', 'random_step', 'far', 'close']
    type_order = types_order[2]
    order = None
    while not all(reached):
        next_moves = nbPlayers*[None]
        prev_j = []
        if 'random' in type_order:
            if order is None:
                order = list(range(nbPlayers))
                random.shuffle(order)
            if 'step' in type_order:
                random.shuffle(order)
        else:
            order = list(range(nbPlayers))
            distances = list(map(lambda idx: manhattan(actual_moves[idx], goalStates[idx]), order))
            if type_order == 'far':
                order = sorted(order, key=lambda idx: distances[idx])
            elif type_order == 'close':
                order = sorted(order, key=lambda idx: distances[idx])[::-1]
        for j in order:
            if reached[j]:
                next_move = actual_moves[j]
            else:
                possible_move = paths[j].pop(0)
                obstacles_1 = next_moves
                obstacles_2 = [actual_moves[k] for k in prev_j if next_moves[k] == actual_moves[j]]
                obstacles = obstacles_1 + obstacles_2

                prev_j.append(j)
                if possible_move in obstacles:
                    print('CONFLICT !!!!!')
                    start = actual_moves[j]
                    destination = paths[j].pop(0)
                    aux_path,a = a_search(start, destination, walls[j] + obstacles)
                    #aux_path.pop(0)
                    num_iter += a
                    paths[j] = aux_path + paths[j]
                    next_move = paths[j].pop(0)
                else:
                    next_move = possible_move
                if next_move == goalStates[j]:
                    reached[j] = True
            next_moves[j] = next_move

        all_moves.append(next_moves)
        actual_moves = next_moves

    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------


    # bon ici on fait juste plusieurs random walker pour exemple...

    posPlayers = initStates
    picked = nbPlayers*[False]
    for moves in all_moves:
        for j in range(nbPlayers):
            players[j].set_rowcol(*moves[j])
            if (not picked[j]):
                score[j] += 1
                if (moves[j] == goalStates[j]):
                    players[j].ramasse(game.layers)
                    picked[j] = True

        game.mainiteration()
    print ("scores:", score)
    print('total score', max(score))
    pygame.quit()





if __name__ == '__main__':
    main()
