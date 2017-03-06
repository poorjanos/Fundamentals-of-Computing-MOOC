"""
A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

import random
import codeskulptor
codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10000

def evaluate_position(num_items):
    """
    Monte Carlo evalation method for Nim
    """
    moves = []
    for move in range(1, MAX_REMOVE + 1, 1):
        wins = 0
        for i in range(TRIALS):
            player = 'Comp'
            heap = int(num_items)
            heap -= move
            
            while heap > 0:
                heap -= random.randint(1,3)
                if player == 'Comp':
                    player = 'Human'
                elif player == 'Human':
                    player = 'Comp'
            
            if player == 'Comp':
                wins += 1
        moves.append(wins)
    probs = [float(i)/float(TRIALS) for i in moves]
    return probs.index(max(probs)) + 1
    


def play_game(start_items):
    """
    Play game of Nim against Monte Carlo bot
    """
    
    current_items = start_items
    print "Starting game with value", current_items
    while True:
        comp_move = evaluate_position(current_items)
        current_items -= comp_move
        print "Computer choose", comp_move, ", current value is", current_items
        if current_items <= 0:
            print "Computer wins"
            break
        player_move = int(input("Enter your current move"))
        current_items -= player_move
        print "Player choose", player_move, ", current value is", current_items
        if current_items <= 0:
            print "Player wins"
            break

play_game(21)
        
    
                 
    