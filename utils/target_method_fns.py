# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:31:00 2019

@author: XXX

This script contains functions to to find stopping points for the target method.
"""

# imports
import numpy as np
from scipy.stats import poisson
import random


# fn to generate target set by randomly sampling documents (without replacement) 
def make_target_set(rel_list, n_docs, target_size):
    range_idxs = [i for i in range(n_docs)]
    target_list = []
    examined_list = []

    while (len(target_list) < target_size) and len(examined_list) < n_docs:
        idx = random.choice(range_idxs)
        range_idxs.remove(idx)
        examined_list.append(idx)

        if rel_list[idx] == 1:
            target_list.append(idx)
           

    return (target_list, examined_list)
    
    
# function to predict stopping point for target method, returns rank stopping pt
def get_stopping_target(target_list, n_docs, target_size):
    
    if len(target_list) == target_size:
        
        i = 0
        target_retrieved = []
        while  (i < n_docs) and (len(target_retrieved) < len(target_list)):
            if i in target_list:
                 target_retrieved.append(i)
            i += 1 

        stop_rank = i-1
               
    else:  # less than target_size rel docs in topic
        stop_rank = n_docs
    
    return stop_rank


# fn to make a list of every doc examined during entire course target method
def get_all_target_examined_idxs(examined_list, tar_stop_n):
    
    all_examined_idxs = [i for i in examined_list]  # docs examined when generating target set
    for i in range(tar_stop_n):  
        if i not in all_examined_idxs:
            all_examined_idxs.append(i)  # add in docs enoucntered when running through ranking
            
    return all_examined_idxs



