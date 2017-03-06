#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Algorithmic Thinking by Rice - Project 1
Created on Mon Jan  2 09:32:14 2017
@author: janos
"""

from collections import Counter

EX_GRAPH0 = {0: set([1,2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3,7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1,2]), 9: set([0,3,4,5,6,7])}



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
        
    
    
def compute_in_degrees(digraph):
    '''
    Takes a directed graph digraph (represented as a dictionary)
    and computes the in-degrees for the nodes in the graph
    '''
    #create and flatten edge lists then Counter
    heads_lists = [value for _, value in digraph.iteritems()]
    heads = [item for sublist in heads_lists for item in sublist]
    heads_count = Counter(heads)
    
    #create keys for ans then load
    keys = [key for key, _ in digraph.iteritems()]
    
    ans = {}
    for key in keys:
        ans[key] =  heads_count[key]
    
    return ans
    

def compute_in_degrees2(digraph):
    '''
    Takes a directed graph digraph (represented as a dictionary)
    and computes the in-degrees for the nodes in the graph
    WITHOUT Counter
    '''
     #initialize variables
    degrees = dict.fromkeys(digraph, 0)
    
    #calculate in-degrees for each node in digraph
    for node in digraph:
        for edge in digraph[node]:
            degrees[edge] += 1

    #return # of total in degrees
    return degrees
    
    
def in_degree_distribution(digraph):
    '''
    Takes a directed graph digraph (represented as a dictionary)
    and computes the unnormalized distribution of the in-degrees of the graph.
    Note that the values in the unnormalized distribution
    returned by this last function are integers, not fractions.
    '''
    indegrees = compute_in_degrees(digraph)
    ans = Counter([values for _, values in indegrees.iteritems()])
    return ans
    
    
 
def in_degree_distribution2(digraph):
    '''
    Takes a directed graph digraph (represented as a dictionary)
    and computes the unnormalized distribution of the in-degrees of the graph.
    Note that the values in the unnormalized distribution
    returned by this last function are integers, not fractions.
    WITHOUT Counter
    '''
    #initialize variables
    computed = compute_in_degrees(digraph)
    distrib = {}
    
    #computes distribution for the in-degrees
    for node in computed:
        degree = computed[node]
        if degree not in distrib:
            distrib[degree] = 1
        else:
            distrib[degree] += 1
    
    #return dictionary of distribution
    return distrib
    
    
    
    
    
    