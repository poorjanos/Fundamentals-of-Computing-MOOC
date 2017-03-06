"""
Cookie Clicker Simulator
"""

#BiuildInfo itt: http://www.codeskulptor.org/#user42_izd1iuMTEe_0.py
#http://www.codeskulptor.org/#user42_izd1iuMTEe_3.py

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = []
        
    def __str__(self):
        return "Total cookies: " + str(self._total_cookies) + '\n' + \
        "Current cookies: " + str(self._current_cookies) + '\n' + \
        "Current time: " + str(self._current_time) + '\n' + \
        "Current cps: " + str(self._current_cps) 
    
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history


    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        missing_cookies = 0.0
        missing_cookies = cookies - self._current_cookies
        if missing_cookies > 0:
            return math.ceil(missing_cookies/self._current_cps)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        self._current_time += time
        self._current_cookies += time * self._current_cps
        self._total_cookies += time * self._current_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))
                
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    b_info = build_info.clone()
    sim_click = ClickerState()
    my_time_left = 0.0
    
    while sim_click.get_time() < duration:
        
        my_time_left = duration - sim_click.get_time()
        item_to_buy = strategy(sim_click.get_cookies(), sim_click.get_cps(), \
                    sim_click.get_history(), my_time_left, b_info)
        
        if item_to_buy is None:
            break
            
#       print "time left: " + str(my_time_left)
#       print "item_to_buy: " + str(item_to_buy)
            
        #determine time_to_wait until purchase (return if exeeds time_left)
        item_cost = b_info.get_cost(item_to_buy)
        time_to_wait = sim_click.time_until(item_cost)
           
#       print "item_cost: " + str(item_cost)
#       print "time_to_wait: " + str(time_to_wait)
        
        if time_to_wait > my_time_left:
            break
        else:
            sim_click.wait(time_to_wait)
            sim_click.buy_item(item_to_buy, item_cost, b_info.get_cps(item_to_buy))
            b_info.update_item(item_to_buy)
                        
#       print sim_click
#       print
    
    if my_time_left > 0:
        sim_click.wait(my_time_left)
        
    return sim_click


#alternatív while feltétellel
def simulate_clicker2(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    info = build_info.clone()
    clicker = ClickerState()
    while duration >= 0:
        item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration, info)

        if item is None:
            break
        
        cost = info.get_cost(item)
        waiting = clicker.time_until(cost)
        
        if duration < waiting:
            break
        else:
            duration -= waiting
            clicker.wait(waiting)
            clicker.buy_item(item, cost, info.get_cps(item))
            info.update_item(item)
    
    clicker.wait(duration)
                             
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    inventory = {}
    item = None
    for item in build_info.build_items():
        inventory[item] = build_info.get_cost(item)
        
    lowest_cost = min(inventory.values())
    
    if cookies + cps * time_left >= lowest_cost:
        for item, cost in inventory.items():
            if cost == lowest_cost:
                return item
    
def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    # for extra exercise, different approach from the one used in strategy_cheap
    inventory = build_info.build_items()
    name = None
    most_expensive = float('-inf')
    resource = cookies + (time_left * cps)

    for item in inventory:
        current_cost = build_info.get_cost(item)
        # still enough time to buy at least one more (most expensive) item
        if current_cost <= resource and most_expensive < current_cost:
            # found currently most expensive item, store it temporarly
            most_expensive = current_cost
            name = item
    return name

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    #print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    #print history
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

