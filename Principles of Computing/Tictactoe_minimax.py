"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win():
        return SCORES[board.check_win()], (-1, -1)
    
    res = []
    possible_moves = board.get_empty_squares()
    for move in possible_moves:
        my_board = board.clone()
        my_board.move(move[0], move[1], player)
        score = mm_move(my_board, provided.switch_player(player))
        if score[0] * SCORES[player] == 1:
            return score[0], move
        res.append(score[0])
    res_invert = [elem * SCORES[player] for elem in res]
    max_val = max(res_invert)
    for idx in range(len(res_invert)):
        if res_invert[idx] == max_val:
            return res[idx], possible_moves[idx]

#chubbypanda
def mm_move2(board, player):
    '''
    make a move on the board,
    
    returns a tuple with two elements; the first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col)
    '''
    # base case, the game is effectively over
    if board.check_win() is not None:
        return SCORES[board.check_win()], (-1, -1)

    # recursion(s)
    # worst possible initial values
    result = (-1, (-1, -1))
    # depth first search along the tree
    for move in board.get_empty_squares():
        copied_board = board.clone()
        copied_board.move(move[0], move[1], player)
        score, _ = mm_move(copied_board, provided.switch_player(player))    # for grader add provided.
        # best possible choice found already
        if score * SCORES[player] == 1:
            return score, move
        # update the initial values
        elif score * SCORES[player] > result[0]:
            result = (score, move)
        elif result[0] == -1:
            result = (result[0], move)
            
    return result[0] * SCORES[player], result[1]
        

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

