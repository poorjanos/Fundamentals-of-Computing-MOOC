#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Algorithmic Thinking by Rice - Project 3
Created on Wed Feb 8 12:22:52 2017
@author: janos
"""

import os
# os.getcwd()
os.chdir('/home/janos/Documents/Rice/algothink_projects/Module_3')

import alg_cluster
import urllib2
import math
from matplotlib import pyplot as plt
import copy

# Create test cases ######################################################


DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
DATA_24_URL = DIRECTORY + "data_clustering/unifiedCancerData_24.csv"

url_dict = dict( (name,eval(name)) for name in ['DATA_24_URL',\
                        'DATA_111_URL','DATA_290_URL','DATA_896_URL', 'DATA_3108_URL'])



def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]
     
  
    
def load_clusters(url_dictionary):
    tbl_names = {}
    tbl_dict = {}
    cluster_dict = {}
    for key, value in url_dictionary.iteritems():
        pos = [n for (n, e) in enumerate(key) if e == '_']
        num = key[pos[0]+1:pos[1]]
        tbl_names[key] = 'data_%s_table' % num
        tbl_dict[tbl_names[key]] = load_data_table(value) 
        cluster_dict[tbl_names[key]] = []
        for idx in range(len(tbl_dict[tbl_names[key]])):
            line = tbl_dict[tbl_names[key]][idx]
            cluster_dict[tbl_names[key]].append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    return cluster_dict
        
cls =  load_clusters(url_dict)
                      

def plot_test_cases(clist, i):
    x = [c.horiz_center() for c in clist[i]]
    y = [c.vert_center() for c in clist[i]]
    plt.plot(x, y, color="black", linestyle='None', marker=".", markersize=6)
    plt.title("Initial clusters")
    plt.show()



# Closest pair functions
def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list
    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    '''
    Brute force closest pair algorithm using alg_cluster.Cluster class methods
    Sweeping through list (base) and comparing (compto) every element to every
    other element (skipping already compared ones)
    '''
    result = [float('inf'), -1, -1]
    for base_idx in range(len(cluster_list)):
        for compto_idx in range(base_idx + 1, len(cluster_list)):
            dist = cluster_list[base_idx].distance(cluster_list[compto_idx])
            if dist < result[0]:
                result[0], result[1], result[2] = dist, min(base_idx, compto_idx), max(base_idx, compto_idx)
    return tuple(result)
                
 
def slow_closest_pair_elegant(cluster_list):
    """
    Elegant solution from the net
    """
    result = (float('inf'), -1, -1)
    list_len = len(cluster_list)
    for idx1 in range(list_len):
        for idx2 in range(list_len):
            if cluster_list[idx1] != cluster_list[idx2]:
                result = min(result, pair_distance(cluster_list, idx1, idx2), key=lambda cluster: cluster[0])
    return result
    
   
def closest_pair_strip(cluster_list, horiz_center, half_width):
    '''
    Helper for FastClosestPair: returns closest pair on different sides of the
    divided space
    Sweeping through list (base) and comparing (compto) every element to next
    three element
    '''
    instrip = [c for c in cluster_list if math.fabs(c.horiz_center() - horiz_center) < half_width]
    instrip.sort(key = lambda cluster: cluster.vert_center())

    result = [float('inf'), -1, -1]
    
    if len(instrip) < 2:
        return tuple(result)
    elif len(instrip) == 2:
        dist = instrip[0].distance(instrip[1])
        if dist < result[0]:
             result[0], result[1], result[2] = dist, min(cluster_list.index(instrip[0]), cluster_list.index(instrip[1])), max(cluster_list.index(instrip[0]), cluster_list.index(instrip[1]))
    else:
        for base_idx in range(len(instrip) - 1):
            '''
            Itt volt egy nagy kavar az elmeleti modul es az owlteszt kozott. Elmeletben 
            az y tengely szerinti sorrendben eleg lett volna +3 pontig keresni. De lehet olyan 
            esetet csinalni, ahol ez nem eleg, es az owltesztben volt is ilyen:
            owltest2 = [alg_cluster.Cluster(set([]), -4.0, 0.0, 1, 0),\
            alg_cluster.Cluster(set([]), 0.0, -1.0, 1, 0),\
            alg_cluster.Cluster(set([]), 0.0, 1.0, 1, 0),\
            alg_cluster.Cluster(set([]), 4.0, 0.0, 1, 0)]
            closest_pair_strip(owltest2, 0.0, 4.1231059999999999)
            '''
            for compto_idx in range(base_idx + 1, min(base_idx + 4, len(instrip))):
                dist = instrip[base_idx].distance(instrip[compto_idx])
                if dist < result[0]:
                    result[0], result[1], result[2] = dist, min(cluster_list.index(instrip[base_idx]), cluster_list.index(instrip[compto_idx])), max(cluster_list.index(instrip[base_idx]), cluster_list.index(instrip[compto_idx]))
    return tuple(result)


def closest_pair_strip_elegant(cluster_list, horiz_center, half_width):
    """
    Elegant solution from the net: extracts only cluster indeces for strip,
    not cluster objects
    """
    strip_idx = [idx for idx in range(len(cluster_list))
                 if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width]
    strip_idx.sort(key=lambda idx: cluster_list[idx].vert_center())
    
    strip_len = len(strip_idx)
    result = (float('inf'), -1, -1)
    
    for idx1 in range(0, strip_len-1):
        for idx2 in range(idx1+1, min(idx1+3, strip_len-1)+1):
            result = min(result, pair_distance(cluster_list, strip_idx[idx1], strip_idx[idx2]),
                         key=lambda cluster: cluster[0])
    return result       

    
def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    sorted_cluster_list = list(cluster_list)
    sorted_cluster_list.sort(key = lambda sorted_cluster_list: sorted_cluster_list.horiz_center())
    
    if len(sorted_cluster_list) <= 3:
        return slow_closest_pair(sorted_cluster_list)
    else:
        mid = len(sorted_cluster_list)/2
        left_half = sorted_cluster_list[:mid]
        right_half = sorted_cluster_list[mid:]
        
        # Call self on both halves
        left_min = fast_closest_pair(left_half)
        right_helper = fast_closest_pair(right_half)
        right_min = tuple([right_helper[0], right_helper[1] + mid, right_helper[2] + mid])
        
        min_so_far = min(left_min, right_min)
       
        # Check for closest pair between points falling on either half
        mid_point = (sorted_cluster_list[len(sorted_cluster_list)/2 -1].horiz_center() + sorted_cluster_list[len(sorted_cluster_list)/2].horiz_center())/2
        min_strip = closest_pair_strip_elegant(sorted_cluster_list, mid_point, min_so_far[0])

    return min(min_so_far, min_strip)


def fast_closest_pair_elegant(cluster_list):
    """
    Elegant solution from the net
    """
    list_len = len(cluster_list)
    if list_len <= 3:
        result = slow_closest_pair_elegant(cluster_list)
    else:
        half_len = list_len / 2
        left_half = [cluster_list[idx] for idx in range(0, half_len)]
        right_half = [cluster_list[idx] for idx in range(half_len, list_len)]
        left_result = fast_closest_pair(left_half)
        right_result = fast_closest_pair(right_half)
        right_result = (right_result[0], right_result[1]+half_len, right_result[2]+half_len)
        temp_result = min(left_result, right_result, key=lambda cluster: cluster[0])
        mid = (cluster_list[half_len-1].horiz_center() + cluster_list[half_len].horiz_center()) / 2
        result = min(temp_result, closest_pair_strip_elegant(cluster_list, mid, temp_result[0]),
                     key=lambda cluster: cluster[0])
        return result


# Owltest valtozat
# http://www.codeskulptor.org/#user42_7yP0uSo4Nt_5.py



######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    
    https://storage.googleapis.com/codeskulptor-alg/img/HW3-HierarchicalClustering.jpg
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key=lambda cluster: cluster.horiz_center())
        closest_pair = fast_closest_pair_elagant(cluster_list)
        cluster_list[closest_pair[1]].merge_clusters(cluster_list[closest_pair[2]])
        cluster_list.pop(closest_pair[2])
    assert len(cluster_list) == num_clusters
    return cluster_list
        

######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    
    https://storage.googleapis.com/codeskulptor-alg/img/HW3-KMeansClustering.jpg
    """

    # position initial clusters at the location of clusters with largest populations
    clist = [cluster for cluster in cluster_list]
    clist.sort(key = lambda cl: cl.total_population())
    initials = clist[-num_clusters:]
    
    while num_iterations:
        result = [alg_cluster.Cluster(set([]),0,0,0,0) for _ in range(num_clusters)]
        
        # add points to clusters
        for clust_idx in range(len(clist)):
            dist = [float('inf'), -1]
            for center_idx in range(len(initials)):
                dist = min(dist, [clist[clust_idx].distance(initials[center_idx]), center_idx],\
                                  key = lambda d: d[0])
            result[dist[1]].merge_clusters(clist[clust_idx])
            
        # recompute initials
        for res_idx in range(len(result)):
            initials[res_idx] = alg_cluster.Cluster(set([]),result[res_idx].horiz_center(),\
                                result[res_idx].vert_center(),0,0)

        num_iterations -= 1
    return result


def kmeans_clustering_elegant(cluster_list, num_clusters, num_iterations):
    """
    Elegant solution from the net
    """
    # position initial clusters at the location of clusters with largest populations
    list_len = len(cluster_list)
    centers = cluster_list[:]
    centers.sort(key=lambda cluster: cluster.total_population(), reverse=True)
    centers = centers[:num_clusters]
    cluster_sets = None
    for dummy_i in range(num_iterations):
        cluster_sets = [alg_cluster.Cluster(set([]), 0.0, 0.0, 0.0, 0.0) for dummy_idx in range(num_clusters)]
        for idx in range(list_len):
            min_idx = min(range(num_clusters), key=lambda center_idx: cluster_list[idx].distance(centers[center_idx]))
            cluster_sets[min_idx].merge_clusters(cluster_list[idx])
        centers = cluster_sets
    return cluster_sets