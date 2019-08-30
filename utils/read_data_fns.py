# -*- coding: utf-8 -*-
"""
Author: Alison Sneyd
Date created: 21/03/2019

This script contains functions to make dictionaries from the relevance and ranking data.
 
"""

import operator


# make dictionary of list of docids relevant to each queryid
def make_rel_dic(qrels_data):
    query_rel_dic = {}
    
    for row in qrels_data:
        row = row.split()
        rel = int(row[3])
        
        if rel == 1:
            query_id = row[0]
            doc_id = row[2]
    
            if query_id not in query_rel_dic.keys():
                query_rel_dic[query_id] = [doc_id]
            else:
                query_rel_dic[query_id].append(doc_id)
                
    return query_rel_dic



# make dictionary of ranked docids for each queryid
def make_rank_dic(run_data):
    doc_rank_dic = {}
    
    for row in run_data:
        row = row.split()
        query_id = row[0]
        doc_id = row[2]
        
        if query_id not in doc_rank_dic.keys():
            doc_rank_dic[query_id] = [doc_id]
        else:
            doc_rank_dic[query_id].append(doc_id)
                
    return doc_rank_dic


# make dic of list relevances of ranked docs for each queryid
def make_rank_rel_dic(query_rel_dic,doc_rank_dic):
    rank_rel_dic = {}
    
    for (query_id, doc_ids) in doc_rank_dic.items():
        rank_rel_dic[query_id] = []
        
        for doc_id in doc_ids:
            if doc_id in query_rel_dic[query_id]:
                doc_rel = 1
            else:
                doc_rel = 0
                
            rank_rel_dic[query_id].append(doc_rel)
            
    return rank_rel_dic


# fn to make list of topics with min size and sort on decreasing size
def make_topics_list(doc_rank_dic, min_topic_size):
    keep_topics = {}  # dic of topic_ids to keep
    
    for key in doc_rank_dic.keys():
        if len(doc_rank_dic[key])>= min_topic_size:
            keep_topics[key] = len(doc_rank_dic[key])
    
    # sort topic ids by decreasing number relevant docs
    sorted_topics = sorted(keep_topics.items(), key=operator.itemgetter(1))[::-1]
    sorted_topics = [topic for (topic, n_dcos) in sorted_topics]
    
    return sorted_topics


# make dictionary of list of docids for each queryid 
def make_query_doc_dic(qrels_data):
    query_doc_dic = {}
    
    for row in qrels_data:
        row = row.split()
        rel = int(row[3])

        query_id = row[0]
        doc_id = row[2]
    
        if query_id not in query_doc_dic.keys():
            query_doc_dic[query_id] = [doc_id]
        else:
            query_doc_dic[query_id].append(doc_id)
                
    return query_doc_dic
