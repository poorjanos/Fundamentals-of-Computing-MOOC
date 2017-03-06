#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Algorithmic Thinking by Rice - Applicaton 2: Network Attack
Created on Mon Jan 23 14:10:38 2017
@author: janos
"""

"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt
from collections import deque


def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

 
def make_complete_graph(num_nodes):
    '''
    Takes the number of nodes num_nodes and returns a dictionary corresponding
    to a complete directed graph with the specified number of nodes.
    A complete graph contains all possible edges subject to the restriction
    that self-loops are not allowed.
    '''
    ans = dict()
    for node in range(num_nodes):
        edges = set(range(num_nodes))
        edges.remove(node)
        ans[node] = edges
    return ans

    
    
class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        Updates the list of node numbers so that each node number
        appears in correct ratio
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        '''
        Main difference to DPA: new node is added to the list len(new_node_neighbors) time,
        since the degree of the newly added node is no longer zero,
        so its chances of being selected in subsequent trials should increase
        '''
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors



##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph
    
#### Helpers to compute graph resilience ##############################

def bfs_visited(ugraph, start_node):
    '''
    Takes an undirected graph and returns visited notes with BFS.
    '''
    # Initialize empty queue
    queue = deque()
    
    # Initialize visited set with start_node
    visited = {start_node}
    
    # Enqueue start_node
    queue.append(start_node)
    
    # BFS
    while queue:
        node = queue.popleft()
        for neighbor in ugraph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited
    
    
def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list of sets, where each
    set consists of all the nodes (and nothing else) in a connected component (CC),
    and there is exactly one set in the list for each connected component in 
    ugraph and nothing else.
    Uses bfs_visited()
    '''
    remaining = set(ugraph.keys())
    cc = []
    
    while remaining:
        # Can pop() instead of random.choice() as item is not needed in 
        # further iterations
        rand_node = remaining.pop()
        con_subset = bfs_visited(ugraph, rand_node)
            
        cc.append(con_subset)
        remaining -= con_subset
            
    return cc
    
    
def largest_cc_size(ugraph):
    '''
    Takes the undirected graph and returns the size (an integer) of
    the largest connected component in graph.
    '''
    cc = cc_visited(ugraph)
    
    if not cc:
        return 0
        
    return max([len(subset) for subset in cc])


def compute_resilience(ugraph, attack_order):
    '''
    Takes the undirected graph, a list of nodes attack_order and
    iterates through the nodes in attack_order. For each node in the list, 
    the function removes the given node and its edges from the graph and
    then computes the size of the largest connected component for the
    resulting graph. The function should return a list whose k+1th entry
    is the size of the largest connected component in the graph after the
    removal of the first k nodes in attack_order. The first entry
    (indexed by zero) is the size of the largest connected component in the
    original graph.
    First two solutions can fail on directed graphs
    '''
    g = copy_graph(ugraph)
    resilience = [largest_cc_size(g)]
    for node in attack_order:
        delete_node(g, node)
        resilience.append(largest_cc_size(g))
    
    return resilience    
    
def compute_resilience2(ugraph, attack_order):
    # Hard copy ugraph and initialize answer list
    g = ugraph.copy()
    lccs = largest_cc_size(g)
    resilience =[lccs]

    for attacked in attack_order:
        # Delete keys and nodes corresponding to attacked node
        # Note: set.remove() and set.discard() are both O(1) but discard does
        # not raise error if item is not in set
        del g[attacked]
        for valuelist in g.values():
            valuelist.discard(attacked)
        # Append to answer list
            resilience.append(largest_cc_size(g))
    
    return resilience

    
def compute_resilience3(graph, attack_order):
    graph = graph.copy()
    resilience = [largest_cc_size(graph)]
    for node in attack_order:
        del graph[node]
        for node2, neighbors in graph.iteritems():
            if node in neighbors:
                graph[node2] = {x for x in neighbors if x != node}
        resilience.append(largest_cc_size(graph))
    return resilience

# ER and UPA generators #######################################################
    
def gen_ER_graph(n, p):
    '''
    Generates random undirected graph with n nodes and p probability per edge
    '''
    graph = {}
    for node in range(n):
        graph[node] = set({})
    for tail in range(n):
        for head in range(n):
            # Key: consider each edge once, hence cannot iterate over the same
            # edge twice. This is achieved by tail < head instead of 
            # tail != edge
            if tail < head and random.random() < p:  
                    graph[tail].add(head)  
                    graph[head].add(tail)
    return graph
    

    
def gen_UPA_graph(n, m):
    '''
    Create n-node random graph with UPA algorithm using UPATrial object 
    to generate neighbors for new nodes from existing nodes
    Preferential attachment (PA) algorithm: the higher indegree a node has, the higher
    chance it has to connect to a new node
    '''
    # Create complete base graph with m nodes and DPATrial object
    graph = make_complete_graph(m)
    trial_obj = UPATrial(m)
    
    # Add new nodes to graph
    for new_node in range(m, n):
        new_neighbours = trial_obj.run_trial(m)
        graph[new_node] = new_neighbours
        for neighbor in new_neighbours:
            graph[neighbor].add(new_node)

    return graph
    

### Question 1 ################################################################

def num_of_edges(ugraph):
    '''
    Computes number of edges in undirected graph
    '''
    return sum([len(value) for key, value in ugraph.iteritems()])/2
    

# Deternine p for ER
PROBS = [n/10000.0 for n in range(10, 50)]

def plot_ER_p(num_nodes, probs):
    '''
    Plot edge numbers for ER graphs with varying probs
    Target: determine starting point for solver
    '''
    # Compute edges num for each prob
    edge_num = []
    for prob in probs:
        rand_ER_graph = gen_ER_graph(num_nodes, prob)
        edge_num.append(num_of_edges(rand_ER_graph))
        
    plt.plot(probs, edge_num, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("ER probs")
    plt.ylabel("Number of edges")
    plt.title("Number of edges as function of probs in ER graph with n = %s" % num_nodes + " nodes")
    plt.show()

    
    
def solver_ER(num_nodes, edge_target, precision, loop_num, start_prob, prob_increase):
    # Set precision bounds
    lower_bound = edge_target * (1 - precision)
    upper_bound = edge_target * (1 + precision)
    
    edge_num = -1
    counter = 0
    
    while counter < loop_num and (edge_num < lower_bound or edge_num > upper_bound):
        rand_ER_graph = gen_ER_graph(num_nodes, start_prob)
        edge_num = num_of_edges(rand_ER_graph)
        start_prob += prob_increase
        counter += 1
        
    if counter <= loop_num-1:
        return (edge_num, start_prob)
    else:
        return "No answer from %s" % loop_num + " loops"
    
# solver_ER(1239, 3047, 0.01, 200, 0.0039, 0.0000001)
# (3051, 0.0039001999999999995)
    
    
# Determine m for UPA
Ms = range(1,10, 1)

def plot_UPA_m(num_nodes, ms):
    '''
    Plot edge numbers for UPA graphs with varying ms
    Target: determine starting point for solver
    '''
    # Compute edges num for each prob
    edge_num = []
    for m in ms:
        rand_UPA_graph = gen_UPA_graph(num_nodes, m)
        edge_num.append(num_of_edges(rand_UPA_graph))
        
    plt.plot(ms, edge_num, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("UPA probs")
    plt.ylabel("Number of edges")
    plt.title("Number of edges as function of probs in UPA graph with n = %s" % num_nodes + " nodes")
    plt.show()
    
# m = 3
 

def random_order(ugraph):
    '''
    Returns nodes of a graph in random order
    '''
    return list(random.sample(ugraph.keys(), len(ugraph.keys())))
    

def main_q1():
    # Load and create graphs
    cnet_graph = load_graph(NETWORK_URL)
    ER_graph = gen_ER_graph(1239, 0.004)
    UPA_graph = gen_UPA_graph(1239, 3)
    
    # Compute random node order for attack
    cnet_random_attack = random_order(cnet_graph)
    ER_random_attack = random_order(ER_graph)
    UPA_random_attack = random_order(UPA_graph)
    
    # Compute resilience
    cnet_res = compute_resilience(cnet_graph, cnet_random_attack)
    ER_res = compute_resilience(ER_graph, ER_random_attack)
    UPA_res = compute_resilience(UPA_graph, UPA_random_attack)
    
    # Plot
    plt.plot(cnet_res, '-b', label='Cnet')
    plt.plot(ER_res, '-r', label='ER p=0.004')
    plt.plot(UPA_res, '-g', label='UPA m=3')
    plt.legend(loc='upper right')
    plt.xlabel("Number of nodes removed")
    plt.ylabel("Size of largest connected component")
    plt.title("Graph resilience simulation with random attack")
    plt.show()
    
    
### Question 3 ################################################################

def fast_targeted_attack(ugraph):
    ugraph = copy_graph(ugraph)
    
    # Compute list DegreeSets where DegreeSets[i] is the set nodes with degree i
    DegreeSets = [set({}) for degree in range(len(ugraph))]
    for node, neighbors in ugraph.iteritems():
        DegreeSets[len(neighbors)].add(node)
    
    NodesToAttack = []
    
    # Iterate over degrees from highest towards lowest
    for degree in range(len(ugraph)-1, -1, -1):
        while DegreeSets[degree]:
            # Choose random max degree node
            max_deg_node = DegreeSets[degree].pop()
            # Update max degree node's neighbors' degree
            for neighbor in ugraph[max_deg_node]:
                neighbor_degree = len(ugraph[neighbor])
                DegreeSets[neighbor_degree].discard(neighbor)
                DegreeSets[neighbor_degree - 1].add(neighbor)
            
            NodesToAttack.append(max_deg_node)
            delete_node(ugraph, max_deg_node)
            
    return NodesToAttack   
    
 
def main_q3():
    '''
    Plot running times of two targeted attack algos on UPA graphs of differing
    size.
    '''
    # UPA graph sizes
    m = 5
    SIZE = range(10, 1000, 10)
    
    # Algo runtimes
    time_base_ta = []
    time_fast_ta = []
    
    # Collect data
    for size in SIZE:
        graph = gen_UPA_graph(size, m)
        
        # Time base
        start = time.time()
        targeted_order(graph)
        end = time.time()
        time_base_ta.append(end - start)
    
        # Time fast
        start = time.time()
        fast_targeted_attack(graph)
        end = time.time()
        time_fast_ta.append(end - start)
    
    # Plot
    plt.plot(SIZE, time_base_ta, '-b', label='Base algo')
    plt.plot(SIZE, time_fast_ta, '-r', label='Fast algo')
    plt.legend(loc='upper right')
    plt.xlabel("Graph size (# of nodes)")
    plt.ylabel("Runtime")
    plt.title("Runnig times of attack algos")
    plt.show()
    
    
### Question 4 ################################################################ 
    
def main_q4():
    # Load and create graphs
    cnet_graph = load_graph(NETWORK_URL)
    ER_graph = gen_ER_graph(1239, 0.004)
    UPA_graph = gen_UPA_graph(1239, 3)
    
    # Compute random node order for attack
    cnet_targeted_attack = fast_targeted_attack(cnet_graph)
    ER_targeted_attack = fast_targeted_attack(ER_graph)
    UPA_targeted_attack = fast_targeted_attack(UPA_graph)
    
    # Compute resilience
    cnet_res = compute_resilience(cnet_graph, cnet_targeted_attack)
    ER_res = compute_resilience(ER_graph, ER_targeted_attack)
    UPA_res = compute_resilience(UPA_graph, UPA_targeted_attack)
    
    # Plot
    plt.plot(cnet_res, '-b', label='Cnet')
    plt.plot(ER_res, '-r', label='ER p=0.004')
    plt.plot(UPA_res, '-g', label='UPA m=3')
    plt.legend(loc='upper right')
    plt.xlabel("Number of nodes removed")
    plt.ylabel("Size of largest connected component")
    plt.title("Graph resilience simulation with targeted attack")
    plt.show()
    
    