# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:31:52 2019

@author: XXX

This script contains functions evaluate stopping fns.
"""

import numpy as np


# fn to calulate recall when retrieve top n docs, input list rel scores & n
def calc_recall(rel_list, n):
    
    num = np.sum(rel_list[0:n])
    denom = np.sum(rel_list)
    if denom > 0:
        rec = round(num/denom,2)
    else:
        rec = 0
    
    return rec



# fn to calculate the acceptability of a single stopping point
def calc_accept(act_recall, des_recall):
    
    if act_recall  >= des_recall:
        accept = 1
    else:
        accept = 0
    
    return accept


# fn to calculate the reliability of a method, input is array of acceptabilities
def calc_reliability(accept_vec):
    
    num = np.sum(accept_vec)
    denom = np.shape(accept_vec)[0]
    prop = round(num/denom,2)
    
    return prop


