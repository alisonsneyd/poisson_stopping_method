# -*- coding: utf-8 -*-
"""
@author: Alison Sneyd

This script runs 3-fold cross validation for the knee method.
"""

# IMPORTS
import numpy as np
import pandas as pd
import math
from scipy.stats import poisson
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import operator
import random
import glob

from utils.read_data_fns import *
from utils.target_method_fns import *  
from utils.knee_method_fns import *   
from utils.inhomogeneous_pp_fns import *   
from utils.eval_fns import *


# read topic relevance data (indep of runs)
with open('data/relevance/qrel_abs_test.txt', 'r') as infile:
    qrels_data = infile.readlines()    
query_rel_dic = make_rel_dic(qrels_data) # make dictionary of list of docids relevant to each queryid
    

# SET PARAMETERS
des_prob = 0.95 # set minimum desired probability for poisson
des_recall = 0.7  # set minimum desired recall level
knee_target_ratio = 6 # knee method rho (Cormack and Grossman set to 6)
knee_adjustments = [0, 25, 50, 100, 150, 200] # adjustments to target ratio


# LOAD AND SPLIT DATA
all_runs = glob.glob('data/runs2017_table3/*/*')
random.seed(1)
random.shuffle(all_runs)
split1 = all_runs[0:11]
split2 = all_runs[11:22]
split3 = all_runs[22:]


# FN TO LOOP OVER RUNS, IMPLEMENTING KNEE METHOD FOR EACH ADJUSTMENT VALUE
def do_knee_method(runs, adjusts):
    run_score_dic = {}
    for run in runs:

        run_name = run[21:]

        with open(run, 'r') as infile:
            run_data = infile.readlines()

        doc_rank_dic = make_rank_dic(run_data)  # make dictionary of ranked docids for each queryid
        rank_rel_dic = make_rank_rel_dic(query_rel_dic,doc_rank_dic) # make dic of list relevances of ranked docs for each queryid

        # LOOP OVER QUERIES
        score_dic = {}
        topics_list = make_topics_list(doc_rank_dic,1)  # sort topics by no docs
        for query_id in topics_list:
            score_dic[query_id] = []

            # EXTRACT COUNTS AND REL LISTS
            n_docs = len(doc_rank_dic[query_id])  # total n. docs in topic
            rel_list = rank_rel_dic[query_id]  # list binary rel of ranked docs   


             # KNEE METHOD
            batches = get_batches(n_docs)

            for adjust in adjusts:
                knee, knee_stop = get_knee_stopping_point_var_adjust(rel_list, batches, knee_target_ratio, adjust)[0:2]
                knee_recall = calc_recall(rel_list, knee_stop)
                knee_effort = knee_stop
                knee_accept = calc_accept(knee_recall, des_recall)
                score_dic[query_id].append((knee_recall, knee_effort, knee_accept))

        accept_vec_dict = {}
        eff_vec_dict = {}
        
        for i, adjust in enumerate(adjusts):    
            accept_vec_dict[str(adjust)+" accept"] = [val[i][2] for val in score_dic.values()]
            eff_vec_dict[str(adjust)+" eff"] = [val[i][1] for val in score_dic.values()]

        topic_size_vec = [len(doc_rank_dic[query_id]) for query_id in topics_list]

        run_score_dic[run_name] = {} 
        for key in accept_vec_dict.keys():
            run_score_dic[run_name][key] = calc_reliability(accept_vec_dict[key])
        for key in eff_vec_dict.keys():    
            run_score_dic[run_name][key] = np.sum(eff_vec_dict[key])
    
    df = pd.DataFrame.from_dict(run_score_dic, orient='index')
    df.loc['Mean']= df.mean()
    df = df.round(2)
    
    return df



# FN TO CALCULATE BEST ASJUSTMENT VALUE
def get_best_adjust(knee_low_rel_adjustments, des_prob, df):
    
    end_scores = df.loc['Mean'].to_dict()

    over_effs = {}
    under_accepts = {}

    for adjust in knee_low_rel_adjustments:
        if end_scores[str(adjust)+" accept"] >= des_prob:
            over_effs[end_scores[str(adjust)+" eff"]] = adjust
        else: 
            under_accepts[end_scores[str(adjust)+" accept"]]  = adjust

    if len(over_effs) > 0:
        min_eff = min(over_effs.keys())
        best_adjust = over_effs[min_eff]

    else:
        max_accept = max(under_accepts.keys())
        best_adjust = under_accepts[max_accept]
        
    return [best_adjust]


# DO 3-FOLD CROSS VALIDATION
df_12 = do_knee_method(split1+split2, knee_adjustments)
best_12 = get_best_adjust(knee_adjustments, des_prob, df_12)
print("Best value on Split 1 + Split 2:", best_12)
df_3 =  do_knee_method(split3, best_12)
print("Result on Split 3:")
print(df_3.loc['Mean'])

df_13 = do_knee_method(split1+split3, knee_adjustments)
best_13 = get_best_adjust(knee_adjustments, des_prob, df_13)
print("Best value on Split 1 + Split 3:", best_13)
df_2 = do_knee_method(split2, best_13)
print("Result on Split 2:")
print(df_2.loc['Mean'])

df_23 = do_knee_method(split2+split3, knee_adjustments)
best_23 = get_best_adjust(knee_adjustments, des_prob, df_23)
print("Best value on Split 2 + Split 3:", best_23)
df_1 = do_knee_method(split1, best_23)
print("Result on Split 1:")
print(df_1.loc['Mean'])
