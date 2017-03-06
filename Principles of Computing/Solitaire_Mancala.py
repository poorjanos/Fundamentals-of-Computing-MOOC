"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        self.board = []
       
    
    def set_board(self, configuration):
        self.board = list(configuration)
       
    
    def __str__(self):
        return str(self.board[::-1])
    
    def get_num_seeds(self, house_num):
        return self.board[house_num]

    def is_game_won(self):
        for idx in range(1, len(self._board)):
            if self._board[idx] != 0:
                return False
        return True
    
    def is_legal_move(self, house_num):
        if house_num > 0 and house_num == self.board[house_num]:
            return True
        return False

    
    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            for i in range(house_num):
                self.board[i] += 1
            self.board[house_num] = 0
            

    def choose_move(self):
        legal_indeces = [i for i in range(len(self.board)) if self.is_legal_move(i) == True]
        if legal_indeces != []:
            return legal_indeces[0]
        return 0
    
    def plan_moves(self):
        save_config = list(self.board)
        start_config = []
        plan = []
        while self.board != start_config:
            start_config = list(self.board)
            plan.append(self.choose_move())
            self.apply_move(self.choose_move()) 
        self.board = save_config
        return plan, start_config, self.board   
        
        #alternative solution:
        #new_board = SolitaireMancala()
        #new_board.set_board(self._board)
        #move_list = []
        #next_move =  new_board.choose_move()
        #while next_move != 0:
        #    new_board.apply_move(next_move)
        #    move_list.append(next_move)
        #    next_move = new_board.choose_move()
        #return move_list



# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """
    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1)   
    
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]

    # add more tests here
    print
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(2), "Expected: False"
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(5), "Expected: True"
    
    #my_game.apply_move(5)
    print
    print "Testing apply_move - Computed:", str(my_game), "Expected:", str([0, 0, 4, 2, 2, 1, 1])

    print
    print my_game.choose_move()
    
    print
    print my_game.plan_moves()
    
test_mancala()


#Import GUI code once you feel your code is correct
import poc_mancala_gui
poc_mancala_gui.run_gui(SolitaireMancala())
