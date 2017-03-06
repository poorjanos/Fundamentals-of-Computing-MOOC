#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Algorithmic Thinking by Rice - Project 2
Created on Mon Jan 16 09:27:43 2017
@author: janos
"""

from collections import deque
import random

EX_GRAPH0 = {0: set([1,2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1,3,4,5]), 1: set([0,2,4,6]), 2: set([1,3,5]), 3: set([0,2]), 
             4: set([0,1]), 5: set([0, 2]), 6: set([1]), 7: set([8]), 8: set([7]),
                9: set([])}
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3,7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1,2]), 9: set([0,3,4,5,6,7])}
             


                         
def bfs_distance(ugraph, start_node):
    '''
    Takes an undirected graph and computes distances for each node from start_node.
    '''
    
    # Initialize empty queue
    queue = deque()
    
    # Initialize distance list with inf for each node
    distance = [float('inf') for key in ugraph.keys()]
                
    # Set start_node distance to 0
    distance[start_node] = 0        
    
    # Enqueue start_node
    queue.append(start_node)
    
    # BFS
    while queue:
        node = queue.popleft()
        for neighbor in ugraph[node]:
            if distance[neighbor] == float('inf'):
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)

    return distance
    
    
def cc_distance(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list of sets, where each
    set consists of all the nodes (and nothing else) in a connected component (CC),
    and there is exactly one set in the list for each connected component in 
    ugraph and nothing else.
    Uses bfs_distance()
    '''
    remaining = set(ugraph.keys())
    cc = []
    
    while remaining:
        # Pick random node and compute dists
        rand_node = random.choice(list(remaining))
        dist = bfs_distance(ugraph, rand_node)
        con_subset = set()
        
        # Add to subset if dist is not inf
        for node in remaining:
            if dist[node] != float('inf'):
                con_subset.add(node)
        
        # Update containers        
        cc.append(con_subset)
        remaining -= con_subset
            
    return cc
    
    
    
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
    '''
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
    
    
    
    
    