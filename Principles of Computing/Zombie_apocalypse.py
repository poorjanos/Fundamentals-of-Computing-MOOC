"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
            # obstacle list was missing! (perhaps intentionally?)
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)     
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
            
    def obstacle(self):
        '''
        generator that yields the list of obstacles
        '''
        for obstacle in self._obstacle_list:
            yield obstacle
        
    def compute_distance_field(self, entity_type):
        '''
        function computes a 2D distance field, distance at member of entity_queue is zero;
        shortest paths avoid obstacles and use distance_type distances
        '''
        # same size as the grid and initialized with artifically high values
        distance_field =[[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] 
                         for dummy_row in range(self._grid_height)]

        # grid visited initialized as to be empty
        visited = poc_grid.Grid(self._grid_height, self._grid_width) # for grader add poc_grid.
        for obstacle in self.obstacle():
            visited.set_full(obstacle[0], obstacle[1])
        
        # creates a copy of the human/zombie list
        boundary = poc_queue.Queue()    # for grader add poc_queue.
        if entity_type == ZOMBIE:
            list_type = self._zombie_list
        elif entity_type == HUMAN:
            list_type = self._human_list

        # check whether the cell is passable and update the neighbor's distance
        for item in list_type:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
        
        #Breath-First Search                
        while len(boundary) > 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
        
        return distance_field

    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_positions = []
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            max_distance = max([zombie_distance_field[neighbor[0]][neighbor[1]] for neighbor in neighbors  \
                                if self.is_empty(neighbor[0], neighbor[1])])

            if zombie_distance_field[human[0]][human[1]] >= max_distance:
                new_positions.append(human)
            elif zombie_distance_field[human[0]][human[1]] < max_distance:
                move = random.choice([neighbor for neighbor in neighbors \
                                     if zombie_distance_field[neighbor[0]][neighbor[1]] == max_distance])
                new_positions.append(move)
        self._human_list = list(new_positions)
                    
                
        
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_positions = []
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            min_distance = min([human_distance_field[neighbor[0]][neighbor[1]] for neighbor in neighbors  \
                                if self.is_empty(neighbor[0], neighbor[1])])

            if human_distance_field[zombie[0]][zombie[1]] <= min_distance:
                new_positions.append(zombie)
            elif human_distance_field[zombie[0]][zombie[1]] > min_distance:
                move = random.choice([neighbor for neighbor in neighbors \
                                     if human_distance_field[neighbor[0]][neighbor[1]] == min_distance])
                new_positions.append(move)
        self._zombie_list = list(new_positions)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
