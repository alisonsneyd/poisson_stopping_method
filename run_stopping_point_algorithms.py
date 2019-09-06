'''
 Author: Alison Sneyd

 This script implements the Poisson process method, target method and knee method over 33 runs for the CLEF2017 dataset and scores them. 

'''

# IMPORTS
import numpy as np
import pandas as pd
import math
from scipy.optimize import curve_fit
import random
import glob
import json


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
sample_props = [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,
                0.7,0.75,0.8,0.85,0.9,0.95,1]  # proportion of docs to sample
min_rel_in_sample = 20 # min number rel docs must be initial sample to proceed with algorithm 
n_windows = 10  # number of windows to male from sample
des_prob = 0.95 # set minimum desired probability for poisson
des_recall = 0.7  # set minimum desired recall level
target_size = 10 # set size target set for target method (Cormack and Grossman set to 10)
knee_rho = 6 # knee method rho (Cormack and Grossman set to 6)





all_runs = glob.glob('data/runs2017_table3/*/*')


# LOOP OVER RUNS
run_score_dic = {}
oracle_dic = {}
for run in all_runs:
    
    run_name = run[21:]
    
    with open(run, 'r') as infile:
        run_data = infile.readlines()
    
    doc_rank_dic = make_rank_dic(run_data)  # make dictionary of ranked docids for each queryid
    rank_rel_dic = make_rank_rel_dic(query_rel_dic,doc_rank_dic) # make dic of list relevances of ranked docs for each queryid

    # LOOP OVER QUERIES
    score_dic = {}
    oracle_dic[run_name] = []
    
    topics_list = make_topics_list(doc_rank_dic,1)  # sort topics by no docs
    for query_id in topics_list:
        score_dic[query_id] = []      
        
        # EXTRACT COUNTS AND REL LISTS
        n_docs = len(doc_rank_dic[query_id])  # total n. docs in topic
        rel_list = rank_rel_dic[query_id]  # list binary rel of ranked docs 
        
        
        # ORACLE
        rel_doc_idxs = np.where(np.array(rel_list) == 1)[0]
        orcale_n_rel = math.ceil(len(rel_doc_idxs)*des_recall)
        oracle_idx = rel_doc_idxs[orcale_n_rel-1]
        oracle_eff = oracle_idx+1
        oracle_dic[run_name].append(oracle_eff)
        
        
        
        # TARGET METHOD
        random.seed(1)
        target_list, examined_list = make_target_set(rel_list, n_docs, target_size)  # get target sample and list all docs examined
        tar_stop_n = get_stopping_target(target_list, n_docs, target_size)  # stopping point
        all_examined_idxs = get_all_target_examined_idxs(examined_list, tar_stop_n)  # list of every doc examined during method
        tar_recall = calc_recall(rel_list, tar_stop_n)
        tar_effort = len(all_examined_idxs) # total effort (inc. sampling)
        tar_accept = calc_accept(tar_recall, des_recall)
        score_dic[query_id].append((tar_recall, tar_effort, tar_accept))
        
        
        # KNEE METHOD
        batches = get_batches(n_docs)
        
        knee, knee_stop = get_knee_stopping_point_var_adjust(rel_list, batches, knee_rho, 150)[0:2]
        knee_recall = calc_recall(rel_list, knee_stop)
        knee_effort = knee_stop
        knee_accept = calc_accept(knee_recall, des_recall)
        score_dic[query_id].append((knee_recall, knee_effort, knee_accept))
        
        knee, knee_stop = get_knee_stopping_point_var_adjust(rel_list, batches, knee_rho, 50)[0:2]
        knee_recall = calc_recall(rel_list, knee_stop)
        knee_effort = knee_stop
        knee_accept = calc_accept(knee_recall, des_recall)
        score_dic[query_id].append((knee_recall, knee_effort, knee_accept))
        
        
        # INHOMOGENEOUS POISSON PROCESS
        # check topic meets initial relevance requirement
        n_samp_docs = int(round(n_docs*sample_props[0]))
        sample_rel_list = rel_list[0:n_samp_docs]  # chunck of rel list examined in sample

        # if meet size requirement run algorithm; else return n_docs as stopping point
        if (np.sum(sample_rel_list) >= min_rel_in_sample):

            windows_end_point = 0
            pred_stop_n = n_docs
            i = 0

            while (i < len(sample_props)) and (pred_stop_n > n_samp_docs):
                sample_prop = sample_props[i]

                n_samp_docs = int(round(n_docs*sample_props[i]))
                sample_rel_list = rel_list[0:n_samp_docs]  # chunck of rel list examined in sample

                # get points
                windows = make_windows(n_windows, sample_prop, n_docs)
                window_size = windows[0][1]

                x,y = get_points(windows, window_size, sample_rel_list)  # calculate points that will be used to fit curve

                try: # try to fit curve
                    p0 = [0.1, 0.001, 1]  # initialise curve parameters
                    opt, pcov = curve_fit(model_func, x, y, p0)  # fit curve
                    a, k, b = opt
                    y2 = model_func(x, a, k, b) # get y-values for fitted curve

                    # check distance between "curves" at end sample
                    n_rel_at_end_samp = np.sum(sample_rel_list)
                    y3 =  model_func(np.array(range(1,len(sample_rel_list)+1)), a, k, b)
                    est_by_curve_end_samp = np.sum(y3)
                    est_by_curve_end_samp = int(round(est_by_curve_end_samp))
                    
                    
                    if n_rel_at_end_samp >= des_recall*est_by_curve_end_samp:
                        
                        # using inhom Poisson process with fitted curve as rate fn, predict total number rel docs in topic 
                        mu = (a/-k)*(math.exp(-k*n_docs)-1)  # integral model_func
                        pred_n_rel = predict_n_rel(des_prob, n_docs, mu) # predict max number rel docs (using poisson cdf)
                        des_n_rel = des_recall*pred_n_rel
                        if des_n_rel <= n_rel_at_end_samp:
                            pred_stop_n = n_rel_at_end_samp             
                  

                except: # if can't fit curve
                    pass
                
                i += 1  # increase sample proportion size


            # score result 
            inhom_recall = calc_recall(rel_list, n_samp_docs)
            inhom_effort = n_samp_docs
            inhom_accept = calc_accept(inhom_recall, des_recall)
            score_dic[query_id].append((inhom_recall, inhom_effort, inhom_accept))


        else: # if not enough rel docs in min sample, stopping point is n_docs
            inhom_recall = calc_recall(rel_list, n_docs)
            inhom_effort = n_docs
            inhom_accept = calc_accept(inhom_recall, des_recall)
            score_dic[query_id].append((inhom_recall, inhom_effort, inhom_accept))

    
    # SCORE RESULTS
    tar_accept_vec = [val[0][2] for val in score_dic.values()]
    knee150_accept_vec = [val[1][2] for val in score_dic.values()]
    knee50_accept_vec = [val[2][2] for val in score_dic.values()]
    inhom_accept_vec = [val[3][2] for val in score_dic.values()]

    tar_eff_vec = [val[0][1] for val in score_dic.values()]
    knee150_eff_vec = [val[1][1] for val in score_dic.values()]
    knee50_eff_vec = [val[2][1] for val in score_dic.values()]
    inhom_eff_vec = [val[3][1] for val in score_dic.values()]

    topic_size_vec = [len(doc_rank_dic[query_id]) for query_id in topics_list]

    run_score_dic[run_name] = {}
    run_score_dic[run_name]['tar rel'] = calc_reliability(tar_accept_vec)
    run_score_dic[run_name]['kn150 rel'] = calc_reliability(knee150_accept_vec)
    run_score_dic[run_name]['kn50 rel'] = calc_reliability(knee50_accept_vec)
    run_score_dic[run_name]['in rel'] = calc_reliability(inhom_accept_vec)
    
    run_score_dic[run_name]['tar tot eff'] =  np.sum(tar_eff_vec)
    run_score_dic[run_name]['kn150 tot eff'] =  np.sum(knee150_eff_vec)
    run_score_dic[run_name]['kn50 tot eff'] =  np.sum(knee50_eff_vec)
    run_score_dic[run_name]['in tot eff'] = np.sum(inhom_eff_vec)
    
    run_score_dic[run_name]['oracle eff'] = np.sum(oracle_dic[run_name])



df = pd.DataFrame.from_dict(run_score_dic, orient='index')
df.loc['Mean']= df.mean()
df = df.round(2)
df.to_json("2017run_scores", orient='records')

print(df.loc['Mean'])

