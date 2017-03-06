#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 12:21:37 2017

@author: janos
"""
import matplotlib.pyplot as plt


l = [5,4,3,6,7]
ll = [5,4,3,2,1]


def inversion_count(alist):
    '''
    Given an array A[0…n−1], an inversion is a pair of indices (i,j) such that
    0≤i<j≤n−1 and A[i]>A[j]
    '''
    inversions = 0
    for i in range(len(alist)-1):
        for j in range(i+1, len(alist)):
            if alist[i] > alist[j]:
                inversions += 1
    return inversions

    
def max_inversions(n):
    '''
    Plot max inversions as function of array size
    '''
    llength = []
    ans = []
    data = []     
    for i in range(n-1):
        alist = range(n, i, -1)
        x = len(alist)
        y = inversion_count(alist)
        llength.append(x)
        ans.append(y)
        data.append((x, y))
    
    plt.plot(llength, llength, '-r', label='Linear')
    plt.plot(llength, [i**2 for i in llength], '-g', label='Quadratic')
    plt.plot(llength, ans, '-b', label='Inversion count')
    plt.legend(loc='upper left')
    plt.xlabel("Size")
    plt.ylabel("Inversion")
    plt.title("Inversion maximums: (n*(n-1))/2")
    plt.show()
    
    # return tuples if needed
    # return data
    
def merge_ordered_lists(blist, clist):
    alist = []
    i = 0
    j = 0
    
    while i < len(blist) and j < len(clist):
        if blist[i] <= clist[j]:
            alist.append(blist[i])
            i += 1
        else:
            alist.append(clist[j])
            j += 1

    if i == len(blist):
        alist += clist[j:]
    else:
        alist += blist[i:]
    
    return alist
 
    

def merge(blist, clist, alist):
    i = 0
    j = 0
    k = 0
    inversion_count = 0
    while i < len(blist) and j < len(clist):
        if blist[i] <= clist[j]:
            alist[k] = blist[i]
            i += 1
        else:
            alist[k] = clist[j]
            j += 1
            inversion_count += len(blist) - i
        
        k += 1

    if i == len(blist):
        alist[k:] = clist[j:]
    else:
        alist[k:] = blist[i:]
    
    return inversion_count



def count_inversions(alist):
    if len(alist) == 1:
        return 0
    else:
        blist = alist[:len(alist)//2]
        clist = alist[len(alist)//2:]
        il = count_inversions(blist)
        ir = count_inversions(clist)
        im = merge(blist, clist, alist)
        print im
    
    return il + ir + im
    


def binary_search(alist, l, r):
    if l > r:
        return -1
    else:
        m = (l + r) / 2
        if alist[m] == m:
            return m
        else:
            if alist[m] < m:
                return binary_search(alist, m + 1, r)
            else:
                return binary_search(alist, l, m - 1)
    
    
def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0  
    
import math
  

  
def closest_pair_unordered(alist):
    mindiff = float('inf')
    for sweep in range(len(alist) - 1):
        for elem in range(sweep + 1, len(alist)):
            diff = math.fabs(alist[sweep] - alist[elem])
            if diff < mindiff:
                mindiff = diff
                cpair = (alist[sweep], alist[elem])
    return cpair
    

def closest_pair_ordered(alist):
    mindiff = float('inf')
    for elem in (range(len(alist) - 1)):
        diff = math.fabs(alist[elem] - alist[elem + 1])
        if diff < mindiff:
                mindiff = diff
                cpair = (alist[elem], alist[elem + 1])
    return cpair
    
    
    

closest_pair_ordered([1,7,9,15,21,100,101])
    
    
    
    