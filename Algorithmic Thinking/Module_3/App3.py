#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:16:45 2017

@author: janos
"""

import os
# os.getcwd()
os.chdir('/home/janos/Documents/Rice/algothink_projects/Module_3')

import alg_cluster
from matplotlib import pyplot as plt
import random
import time



def gen_random_clusters(num_clusters):
    return [alg_cluster.Cluster(set([]),random.random(),random.random(),0,0)\
            for _ in range(num_clusters)]
    
def timer(max_clusters, myfunc):
    clust_size = range(2, max_clusters + 1)
    
    runtimes = []
    for size in clust_size:
        cluster_list = gen_random_clusters(size)
        cluster_list.sort(key = lambda cluster_list: cluster_list.horiz_center())
        
        start = time.time()
        
        myfunc(cluster_list)
        
        end = time.time()
        runtimes.append(end - start)
    
    plt.plot(clust_size, runtimes, color="black", linestyle='None', marker=".", markersize=6)
    plt.title("Runtimes of %s" % myfunc)
    plt.show()
    