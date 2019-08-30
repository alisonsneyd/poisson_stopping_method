# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:31:00 2019

@author: Alison Sneyd

This script contains functions to find stopping points for the inhomogeneous Poisson process.
"""

# imports
import numpy as np
from scipy.stats import poisson
import random



# fn to define windows of indexes to examine 
def make_windows(n_windows, sample_prop, n_docs):

    n_samp_docs = int(round(n_docs*sample_prop))
    window_size = int(n_samp_docs/n_windows)
    w_e = window_size  # end index current last window
    windows = [(0,w_e)]  # window (x,y) = window from rank x+1 to idx y

    while w_e < n_samp_docs:
        w_s =  windows[-1][-1] 
        w_e = w_s  + window_size 
        windows.append((w_s,w_e))
    
    windows = windows[:-1]

    return(windows)
    
    
 # fn to calculate points that will be used to fit curve
def get_points(windows, window_size, rel_list):

    # x-values are midpoints between start and end of windows
    x = [round(np.mean([w_s,w_e])) for (w_s,w_e) in windows]

    # y-values are the rate at which relevant documents occur in the window
    # ex: rate 0.1 = 0.1 rel docs per doc, or 1 in 10 docs are relevant
    y = [np.sum(rel_list[w_s:w_e]) for (w_s,w_e) in windows]
    y = [y_i/window_size for y_i in y]

    # convert lists to numpy arrays
    x = np.array(x)
    y = np.array(y)

    return (x,y)


# fn to fit curve to points
def model_func(x, a, k, b): # x = vector x values
    return a*np.exp(-k*x) 


 # function to predict max number of relevant documents
def predict_n_rel(des_prob, n_docs, mu):

    i = 0
    cum_prob = poisson.cdf(i, mu)
    while  (i < n_docs) and (cum_prob < des_prob):
        i += 1 
        cum_prob = poisson.cdf(i, mu)

    return i


# function to predict stopping point for inhom pp using rel list, returns rank stopping pt
def get_stopping_inhom(des_recall, pred_n_rel, rel_list, n_docs):

    des_n_rel = des_recall*pred_n_rel

    i = 0
    n_rel_retrieved = 0
    while  (i < n_docs) and (n_rel_retrieved < int(round(des_n_rel))):
        if rel_list[i] == 1:
            n_rel_retrieved += 1
        i += 1 

    stop_rank = i-1

    return stop_rank
            
