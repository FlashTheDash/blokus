#!/usr/bin/env python3

# the * import should be safe because there are no global variables
# in blokus_core
from blokus_core import *
import copy

def main():
    play_game(1)

def play_game(human_players=4, ai_players=0):
    board = Board(human_players)
    
    moves_not_made = 0
    for player in board.players:
        print(player.color)

        if player.choose_move(board): # returns False if no move made
            moves_not_made = 0
        else:
            moves_not_made += 1
        
        print(board.spaces)

        if moves_not_made == len(board.players):
            # game over
            break
    
    # finish scoring

    # sort players into list of highest score first
    board.players.sort(key=lambda x: -x.score)
    # print that out, maybe do something else with this later
    print('Game Over!')
    print('Winner: ' + board.players[0].color)
    # TODO: should "probably" also handle ties

if __name__ == '__main__':
    main()
