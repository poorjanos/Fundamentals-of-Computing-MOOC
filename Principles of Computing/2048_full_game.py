"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(nums):
    prev = None
    store = []

    for next_ in nums:
        if not next_:
            continue
        if prev is None:
            prev = next_
        elif prev == next_:
            store.append(prev + next_)
            prev = None
        else:
            store.append(prev)
            prev = next_
    if prev is not None:
        store.append(prev)
    store.extend([0] * (len(nums) - len(store)))
    return store

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.reset()
        self.initials = dict()
        self.initials[UP] = [(0, idx) for idx in range(self.width)]
        self.initials[DOWN] = [(self.height-1, idx) for idx in range(self.width)]
        self.initials[LEFT] = [(idx, 0) for idx in range(self.height)]
        self.initials[RIGHT] = [(idx, self.width-1) for idx in range(self.height)]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = [[0 for idx_w in range(self.width)] for idx_h in range(self.height)]
        self.new_tile()
        self.new_tile()
       

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return '\n'.join(map(str, self.grid))
    

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        change_counter = 0
        for cell in self.initials[direction]:
            cells = []
            cell_idx = list(cell)
            it_max = 0
            if direction <= 2:
                it_max = self.height
            else:
                it_max = self.width
            #compute cells in row or column
            for step in range(it_max):
                cells.append(cell_idx)
                cell_idx = [i+j for i,j in zip(cell_idx, OFFSETS[direction])]
            #extract values
            values = []
            for cell in cells:
                values.append(self.get_tile(cell[0], cell[1]))
            #merge
            merged_values = merge(values)
            #insert merged values
            v = 0
            for cell in cells:
                if self.get_tile(cell[0], cell[1]) != merged_values[v]:
                    change_counter += 1
                self.set_tile(cell[0], cell[1], merged_values[v])
                v += 1
                
        if change_counter > 0:
                self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zeroes = [(idx_h, idx_w) for idx_h in range(self.height) for idx_w in range(self.width) 
                       if self.grid[idx_h][idx_w]==0]
        zero_tuple = random.choice(zeroes)
        self.grid[zero_tuple[0]][zero_tuple[1]] = random.choice([2,2,2,2,2,2,2,2,2,4])

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]

ng = TwentyFortyEight(2,2)
print ng

ng.reset()
print ng
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
