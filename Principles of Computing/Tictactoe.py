"""
# Mini-project #3 - Monte Carlo Tic-Tac-Toe Player
# as a Coursera's "Principles of computing"
# course assignment.
# Author: Sergey Korytnik
# Date: 12th August 2016
#
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided
import time

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 300         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial_impl(board, player, empty_squares):
    """
    This function takes a current board and the next player to move.
    The function plays a game starting with the given player 
    by making random moves, alternating between players.
    The function returns when the game is over. 
    The modified board contains the state of the game,
    The function returns state of the game (PALYERX,PLAYERO or DRAW).
    """
    dim = board.get_dim()
    num_occupied = dim * dim - len(empty_squares)
    lower_check_limit = dim + dim - 1 
    
    random.shuffle(empty_squares)
    for (row,col) in empty_squares:
        board.move(row, col, player)
        num_occupied += 1
        if num_occupied >= lower_check_limit:
            game_status = board.check_win()
            if game_status != None:
                return game_status        
        player = provided.switch_player(player)
    return provided.DRAW

def mc_trial(board, player):
    """
    This fucnction just calls mc_trial_impl and ignores its return value.
    The function must make the machine grader happy.
    """
    mc_trial_impl(board, player, board.get_empty_squares())

def mc_update_scores_impl(scores, board, player, winner):
    """
    This function takes a grid of scores (a list of lists)
    with the same dimensions as the Tic-Tac-Toe board,
    a board from a completed game, which player 
    the machine player is and winner of the current game.
    The function scores the completed board and updates 
    the scores grid. As the function updates the scores
    grid directly, it does not return anything.
    """    
    if player == provided.PLAYERX:
        player_x_score = SCORE_CURRENT
        player_o_score = -SCORE_OTHER
    else:
        player_o_score = SCORE_CURRENT
        player_x_score = -SCORE_OTHER
        
    if player != winner:
        player_o_score = - player_o_score
        player_x_score = - player_x_score
        
    dim = board.get_dim()    
    for (row_index, row) in enumerate(scores):
        for col_index in xrange(dim):
            square = board.square(row_index, col_index)
            if square == provided.PLAYERX:
                row[col_index] += player_x_score
            elif square == provided.PLAYERO:
                row[col_index] += player_o_score

    
def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists)
    with the same dimensions as the Tic-Tac-Toe board,
    a board from a completed game, and which player 
    the machine player is. The function scores the completed
    board and updates the scores grid. As the function
    updates the scores grid directly,
    it does not return anything.
    """
    winner = board.check_win()
    if winner != provided.DRAW:
        mc_update_scores_impl(scores, board, player, winner)

def get_max_score(scores, empty_squares):
    """
    finds a maximum value (score) in a grid of scores for 
    elements of the grid listed in empty_squares 
    (list of tuples (row,col))
    """
    return max( map(
            lambda rowcol: scores[rowcol[0]][rowcol[1]],
            empty_squares)
        )
        
def get_best_move_impl(scores, empty_squares):
    """
    This function takes a grid of scores and list
    of tuples (row col) referencing elements in the grid.
    The function finds all of the elements with the 
    maximum score and randomly returns one of them as 
    a (row, column) tuple. It is an error to call this 
    function with a board that has no empty squares 
    (there is no possible next move), so your function
    may do whatever it wants in that case.     
    """
    
    max_score = get_max_score(scores, empty_squares)
    max_score_candidates = filter(
            lambda rowcol: scores[rowcol[0]][rowcol[1]] == max_score,
            empty_squares) 
    return random.choice(max_score_candidates)                                                      

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    The function finds all of the empty squares with the 
    maximum score and randomly returns one of them as 
    a (row, column) tuple. It is an error to call this 
    function with a board that has no empty squares 
    (there is no possible next move), so your function
    may do whatever it wants in that case.     
    """
    return get_best_move_impl(
        scores,
        board.get_empty_squares()
    )

def mc_move(board, player, trials):
    """
    This function takes a current board,
    which player the machine player is,
    and the number of trials to run.
    The function uses the Monte Carlo 
    simulation described above to return 
    a move for the machine player in the
    form of a (row, column) tuple.    
    """
    empty_squares = board.get_empty_squares()
    dim = board.get_dim()
    scores = [ [0] * dim for dummy_index in range(dim) ]
    for dummy_index in xrange(trials):
        test_board = board.clone()
        status = mc_trial_impl(
            test_board,
            player,
            empty_squares
        )
        if status != provided.DRAW:
            mc_update_scores_impl(
                scores,
                test_board,
                player,
                status
            )
    return get_best_move_impl(scores, empty_squares)
            
def performance_test():
    """
    the performance test borrowed from
    http://www.codeskulptor.org/#user41_rAX7Nukse9WzOOV.py    
    """    
    time.time()
    start = time.time()
    provided.play_game(mc_move, NTRIALS, False)
    print str(provided.play_game)+":   \t" + str( (time.time() - start) )

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(4, provided.PLAYERX, mc_move, NTRIALS, False)   
performance_test()