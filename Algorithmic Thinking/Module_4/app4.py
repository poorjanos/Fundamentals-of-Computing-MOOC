#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Algorithmic Thinking by Rice - Application 4
Created on Thu Mar  2 08:34:50 2017
@author: janos
"""
import os
# os.getcwd()
os.chdir('/home/janos/Documents/Rice/algothink_projects/Module_4')


DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import alg_project4_solution as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


# Question 1 ##################################################################

HUMAN_EYELESS = read_protein(HUMAN_EYELESS_URL)
FRUITFLY_EYELESS = read_protein(FRUITFLY_EYELESS_URL)
SCORING_MATRIX = read_scoring_matrix(PAM50_URL)
ALIGNMENT_MATRIX = student.compute_alignment_matrix(HUMAN_EYELESS, \
                                                    FRUITFLY_EYELESS,\
                                                    SCORING_MATRIX, False)

student.compute_local_alignment(HUMAN_EYELESS, FRUITFLY_EYELESS,\
                                SCORING_MATRIX, ALIGNMENT_MATRIX)

# Question 2 ##################################################################
PAX = read_protein(CONSENSUS_PAX_URL)

loc_score, loc_human, loc_fly = student.compute_local_alignment(HUMAN_EYELESS,\
                                                               FRUITFLY_EYELESS,\
                                                               SCORING_MATRIX,\
                                                               ALIGNMENT_MATRIX)

for align in (loc_human, loc_fly):
    align = align.replace('-', '')
    alignment_matrix = student.compute_alignment_matrix(align, PAX, SCORING_MATRIX, True)
    score, alignment, cons = student.compute_global_alignment(align, PAX, SCORING_MATRIX, alignment_matrix)
    print sum([alignment[i] == cons[i] for i in range(len(alignment))]) / float(len(alignment))


# Question 4 ##################################################################


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    scoring_distribution = {}
    list_y = list(seq_y)
    for trial in range(num_trials):
        temp_y = list_y
        random.shuffle(temp_y)
        rand_y = ''.join(temp_y)
        alignment_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score, _, _ = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)
        scoring_distribution[score] = scoring_distribution.get(score, 0) + 1
    return scoring_distribution
    
    
sc_dist = generate_null_distribution(HUMAN_EYELESS, FRUITFLY_EYELESS, SCORING_MATRIX, 1000)



plt.bar(sc_dist.keys(),\
         list(map(lambda value: value / float(1000), sc_dist.values())))
plt.xlabel('score')
plt.ylabel('fraction of total trials')
plt.title('Normalized Score Distribution')
plt.show()

# Question 5 ##################################################################

mu = sum([key*value for key, value in sc_dist.iteritems()])/1000
sigma = math.sqrt(sum([((key - mu)**2) * value for key, value in sc_dist.iteritems()])/1000)
z = (loc_score - mu) / sigma



