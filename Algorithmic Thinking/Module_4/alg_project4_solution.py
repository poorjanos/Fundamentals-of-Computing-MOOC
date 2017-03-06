#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Algorithmic Thinking by Rice - Project 4
Created on Tue Feb 28 14:25:41 2017
@author: janos
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Return a scoring matrix as dict of dicts depending on the input score
    and alphabet set
    """
    alp = set(alphabet)
    alp.add('-')
    result = dict()
    for char_a in alp:
        row_result = dict()
        for char_b in alp:
            if char_a == '-' or char_b == '-':
                row_result[char_b] = dash_score
            elif char_a == char_b:
                row_result[char_b] = diag_score
            else:
                row_result[char_b] = off_diag_score
        result[char_a] = row_result
    return result


SCORING_MATRIX = build_scoring_matrix(['A','C','T','G'],5,2,-2)



def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Return a global or local alignment matrix of seq_x and seq_y
    """
    len_x, len_y = len(seq_x), len(seq_y)
    amatrix = [[0 for _ in range(len_y+1)] for _ in range(len_x+1)]
    
    for row in range(1, len_x+1):
        amatrix[row][0] = amatrix[row-1][0] + scoring_matrix[seq_x[row-1]]['-']
        if not global_flag and amatrix[row][0] < 0:
            amatrix[row][0] = 0
    
    for col in range(1, len_y+1):
        amatrix[0][col] = amatrix[0][col-1] + scoring_matrix[seq_y[col-1]]['-']
        if not global_flag and amatrix[0][col] < 0:
            amatrix[0][col] = 0
    
    for row in range(1, len_x+1):
        for col in range(1, len_y+1):
            amatrix[row][col] = max(amatrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]],
                                    amatrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-'],
                                    amatrix[row][col-1] + scoring_matrix[seq_y[col-1]]['-'])
            if not global_flag and amatrix[row][col] < 0:
                amatrix[row][col] = 0                          
    
    return amatrix


GLOBAL_ALIGNMENT_MATRIX = compute_alignment_matrix('AC', 'TAG', SCORING_MATRIX, True)
LOCAL_ALIGNMENT_MATRIX = compute_alignment_matrix('AC', 'TAG', SCORING_MATRIX, False)


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Return the global alignment of seq_x and seq_y
    """
    row = len(seq_x)
    col = len(seq_y)
    align_x = ''
    align_y = ''
    
    while row != 0 and col != 0:
        if alignment_matrix[row][col] == alignment_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]]:
            align_x = seq_x[row-1] + align_x
            align_y = seq_y[col-1] + align_y
            row -= 1
            col -= 1
        else:
            if alignment_matrix[row][col] == alignment_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-']:
                align_x = seq_x[row-1] + align_x
                align_y = '-' + align_y
                row -= 1
            else:
                align_x = '-' + align_x
                align_y =  seq_y[col-1] + align_y
                col -= 1
    
    while row != 0:
        align_x = seq_x[row-1] + align_x
        align_y = '-' + align_y
        row -= 1
        
    while col != 0:
        align_x = '-' + align_x
        align_y = seq_y[col-1] + align_y
        col -= 1
        
    return alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y



compute_global_alignment('AC', 'TAG', SCORING_MATRIX, GLOBAL_ALIGNMENT_MATRIX)



def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Return the local alignment of seq_x, seq_y
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    
    max_pos = (-1, -1)
    max_score = float('-inf')
    for row in range(len_x+1):
        for col in range(len_y+1):
            if alignment_matrix[row][col] > max_score:
                max_score = alignment_matrix[row][col]
                max_pos = (row, col)
    
    align_x = ''
    align_y = ''
    row, col = max_pos
    
    while alignment_matrix[row][col] != 0:
        if alignment_matrix[row][col] == alignment_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]]:
            align_x = seq_x[row-1] + align_x
            align_y = seq_y[col-1] + align_y
            row -= 1
            col -= 1
        else:
            if alignment_matrix[row][col] == alignment_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-']:
                align_x = seq_x[row-1] + align_x
                align_y = '-' + align_y
                row -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[col-1] + align_y
                col -= 1
    
    return max_score, align_x, align_y


compute_local_alignment('AC', 'TAG', SCORING_MATRIX, LOCAL_ALIGNMENT_MATRIX)