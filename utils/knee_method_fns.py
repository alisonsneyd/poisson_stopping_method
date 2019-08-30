# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:31:00 2019

@author: XXX

This script contains functions to find stopping points for the knee method.
"""

# imports
import numpy as np
import math

# get batches as defined by autonomous tar method (Cormack and Grossman, 2015)
def get_batches(n_docs):
    
    a = 1
    batches = []
    
    while a < n_docs:
        batches.append(a)
        a += math.ceil(a/10)
        
    return batches


# fn to find the knee i for a given value of s
def find_knee(rel_list, s):
    
    n_rel = np.sum(rel_list[0:s])
    m = n_rel/s  # slope of line connecting (s, n_rel) to origin
    
    distances = []
    for x_r in range(1,s+1): # x-values = rank
        y_r = np.sum(rel_list[0:x_r])  # get corresponding y-value on gain curve
        distance = (abs(m*x_r - y_r))/math.sqrt(m**2 + 1)  # standard formula dist point to line
        distances.append(distance)
        
    max_distance_rank = distances.index(max(distances))+1  # get rank of max distance
            
    return max_distance_rank


# fn to calculate the slope ratio given i and s
def get_slope_ratio(rel_list, i,s):  # get rho pg 5 Cormack and Grossman, i < s
    
    big_num = (np.sum(rel_list[0:i]))/i
    big_denom = (1 + np.sum(rel_list[i:s]))/(s - i)
    rho = big_num/big_denom
    
    return rho


# fn to get the stopping point for the knee method
def get_knee_stopping_point_var_adjust(rel_list, batches, target_ratio, low_rel_adjust):
    
    idx = 0
    rho = 0
    adjusted_ratio = low_rel_adjust + target_ratio
    
    while (rho < adjusted_ratio) and (idx < len(batches)):
    
        s = batches[idx]
        i = find_knee(rel_list, s)
        
        relret = np.sum(rel_list[0:i])
        adjusted_ratio = low_rel_adjust + target_ratio - min(relret, low_rel_adjust)
        
        if i < s:
            rho = get_slope_ratio(rel_list, i,s)
        else:
            rho = 0

        idx += 1

    return (i,s)  # knee of stopping point, stopping point
