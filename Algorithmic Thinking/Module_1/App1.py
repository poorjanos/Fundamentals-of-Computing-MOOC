#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Algorithmic Thinking by Rice - Applicaton 1: Citation Graph
Created on Tue Jan  3 07:58:23 2017
@author: janos
"""

import urllib2
from collections import Counter
import matplotlib.pyplot as plt
import random

# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

    
# Create citation graph    
citation_graph = load_graph(CITATION_URL)
# Get a partial view of the dict with:
# dict(citation_graph.items()[0:10])


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
    
# Create unnormalized in_degree dict
dist = in_degree_distribution(citation_graph)
# Get a partial view of the dict with:
# dict(dist.items()[0:10])



########### Question 1 ###############################################

# Normaize in_degree dict:
def normalize_degrees(adict):
    '''
    Takes an unnormalized in_degree dict and returns a normalized one
    '''
    nodes_sum = sum(adict.values())
    
    ans = {}
    for node in adict:
        ans[node] = float(adict[node]) / nodes_sum
    
    return ans
        
    
# Create normalized in_degree dict
normdist = normalize_degrees(dist)
# Get a partial view of the dict with:
# dict(normdist.items()[0:10])
    
    
# Create loglog plot
def plot_normalized(normal_distrib):
    x_vals = []
    y_vals = []
    for degree in normal_distrib:
        x_vals.append(degree)
        y_vals.append(normal_distrib[degree])
    plt.loglog(x_vals, y_vals, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log of Number of Degrees")
    plt.ylabel("Log of Distribution")
    plt.title("Log/log Normalized Distribution of High Energy Physics Theory Papers")
    plt.show()
    
plot_normalized(normdist)
    


########### Question 2 ###############################################
 
def gen_random_digraph(n, p):
    '''
    Generates random digraph with n nodes and p probability per edge
    '''
    graph = {}
    for tail in range(n):
        graph[tail] = []
        for head in range(n):
            if tail != head and random.random() < p:  
                    graph[tail].append(head)  
    return graph


def plot_random_distributions(numnodes, prob):
    graph = gen_random_digraph(numnodes, prob)
    graph_in_degree_dist = in_degree_distribution(graph)
    graph_in_degree_dist_norm = normalize_degrees(graph_in_degree_dist)
    
    x_vals = []
    y_vals = []
    for degree in graph_in_degree_dist_norm:
        x_vals.append(degree)
        y_vals.append(graph_in_degree_dist_norm[degree])
    plt.loglog(x_vals, y_vals, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log of Number of Degrees")
    plt.ylabel("Log of Distribution")
    plt.title("Log/log Normalized Distribution of Random Digraph (prob = %s" % prob + ")")
    plt.show()
    
    
########### Question 3-4-5 ############################################### 
'''
Helper function to make complete graph
'''

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


"""
Provided code for application portion of module 1
Helper class for implementing efficient version
of DPA algorithm
"""

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]

    def __str__(self):
        return str(self._node_numbers)
    
    def run_trial(self, num_nodes):
        """
        Conduct num_node trials by applying random.choice()
        to the list of node numbers
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        '''
        Main difference to UPA: new node is added to the list 1 time,
        since the degree of the newly added node is zero,
        but it should have a chance to be selected in subsequent trials
        '''
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
def gen_DPA_graph(n, m):
    '''
    Create n-node random digraph with DPA algorithm using DPATrial object 
    to generate neighbors for new nodes from existing nodes
    Preferential attachment (PA) algorithm: the higher indegree a node has, the higher
    chance it has to connect to a new node
    '''
    # Create complete base graph with m nodes and DPATrial object
    graph = make_complete_graph(m)
    trial_obj = DPATrial(m)
    
    # Add new nodes to graph
    for new_node in range(m, n):
        new_neighbours = trial_obj.run_trial(m)
        graph[new_node] = new_neighbours

    return graph
    

def plot_DPA(n, m):
    graph = gen_DPA_graph(n, m)
    graph_in_degree_dist = in_degree_distribution(graph)
    graph_in_degree_dist_norm = normalize_degrees(graph_in_degree_dist)
    
    x_vals = []
    y_vals = []
    for degree in graph_in_degree_dist_norm:
        x_vals.append(degree)
        y_vals.append(graph_in_degree_dist_norm[degree])
    plt.loglog(x_vals, y_vals, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log of Number of Degrees")
    plt.ylabel("Log of Distribution")
    plt.title("Log/log Normalized Distribution of Random DPA Digraph (n = %s" % n + "m = %s" % m + ")")
    plt.show()
    
plot_DPA(28000, 13) 
    
    
    
    
    
    
    