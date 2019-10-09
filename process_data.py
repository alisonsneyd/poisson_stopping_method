# -*- coding: utf-8 -*-
"""
@author: Alison Sneyd
This code copies the relevant files from https://github.com/CLEF-TAR/tar to a
new directory. 
"""

# IMPORTS
import os
from shutil import copy
import glob


# COPY RELEVANCE FILE
wd = os.getcwd()
os.mkdir("data/relevance")
#os.mkdir(os.path.join(wd, "data/relevance"))
copy('data/tar-master/2017-TAR/testing/qrels/qrel_abs_test.txt', 'data/relevance/')


# COPY RUNS
os.mkdir("data/runs2017_table3")
os.mkdir("data/runs2017_table3/AMC/")
copy("data/tar-master/2017-TAR/participant-runs/AMC/clef-finals/amc.run.res", "data/runs2017_table3/AMC")


os.mkdir("data/runs2017_table3/AUTH/")
copy("data/tar-master/2017-TAR/participant-runs/AUTH/simple-eval/run-1", "data/runs2017_table3/AUTH")
copy("data/tar-master/2017-TAR/participant-runs/AUTH/simple-eval/run-2", "data/runs2017_table3/AUTH")
copy("data/tar-master/2017-TAR/participant-runs/AUTH/simple-eval/run-3", "data/runs2017_table3/AUTH")
copy("data/tar-master/2017-TAR/participant-runs/AUTH/simple-eval/run-4", "data/runs2017_table3/AUTH")


os.mkdir("data/runs2017_table3/CNRS/")
copy("data/tar-master/2017-TAR/participant-runs/CNRS/trec_abrupt_ALL", "data/runs2017_table3/CNRS")
copy("data/tar-master/2017-TAR/participant-runs/CNRS/trec_gradual_ALL", "data/runs2017_table3/CNRS")
copy("data/tar-master/2017-TAR/participant-runs/CNRS/trec_no_AF_ALL", "data/runs2017_table3/CNRS")
copy("data/tar-master/2017-TAR/participant-runs/CNRS/trec_no_AF_full_ALL", "data/runs2017_table3/CNRS")

os.mkdir("data/runs2017_table3/ECNU/")
copy("data/tar-master/2017-TAR/participant-runs/ECNU/run1.res.txt", "data/runs2017_table3/ECNU")


os.mkdir("data/runs2017_table3/NTU/")
copy("data/tar-master/2017-TAR/participant-runs/NTU/test_ranked_run_1.txt", "data/runs2017_table3/NTU")
copy("data/tar-master/2017-TAR/participant-runs/NTU/test_ranked_run_2.txt", "data/runs2017_table3/NTU")
copy("data/tar-master/2017-TAR/participant-runs/NTU/test_ranked_run_3.txt", "data/runs2017_table3/NTU")


os.mkdir("data/runs2017_table3/Padua/")
copy("data/tar-master/2017-TAR/participant-runs/Padua/simple/ims_iafa_m10k150f0m10", "data/runs2017_table3/Padua")
copy("data/tar-master/2017-TAR/participant-runs/Padua/simple/ims_iafap_m10p2f0m10", "data/runs2017_table3/Padua")
copy("data/tar-master/2017-TAR/participant-runs/Padua/simple/ims_iafap_m10p5f0m10", "data/runs2017_table3/Padua")
copy("data/tar-master/2017-TAR/participant-runs/Padua/simple/ims_iafas_m10k50f0m10", "data/runs2017_table3/Padua")


os.mkdir("data/runs2017_table3/QUT/")
copy("data/tar-master/2017-TAR/participant-runs/QUT/coordinateascent_result_bool_ltr_test.txt", "data/runs2017_table3/QUT")
copy("data/tar-master/2017-TAR/participant-runs/QUT/coordinateascent_result_pico_ltr_test.txt", "data/runs2017_table3/QUT")
copy("data/tar-master/2017-TAR/participant-runs/QUT/randomforest_result_bool_ltr_test.txt", "data/runs2017_table3/QUT")
copy("data/tar-master/2017-TAR/participant-runs/QUT/randomforest_result_pico_ltr_test.txt", "data/runs2017_table3/QUT")


os.mkdir("data/runs2017_table3/Sheffield/")
copy("data/tar-master/2017-TAR/participant-runs/Sheffield/Test_Data_Sheffield-run-1", "data/runs2017_table3/Sheffield")
copy("data/tar-master/2017-TAR/participant-runs/Sheffield/Test_Data_Sheffield-run-2", "data/runs2017_table3/Sheffield")
copy("data/tar-master/2017-TAR/participant-runs/Sheffield/Test_Data_Sheffield-run-3", "data/runs2017_table3/Sheffield")
copy("data/tar-master/2017-TAR/participant-runs/Sheffield/Test_Data_Sheffield-run-4", "data/runs2017_table3/Sheffield")


os.mkdir("data/runs2017_table3/UCL/")
copy("data/tar-master/2017-TAR/participant-runs/UCL/run_abstract_test.txt", "data/runs2017_table3/UCL")
copy("data/tar-master/2017-TAR/participant-runs/UCL/run_fulltext_test.txt", "data/runs2017_table3/UCL")

os.mkdir("data/runs2017_table3/UOS-test/")
copy("data/tar-master/2017-TAR/participant-runs/UOS/test/sis.TMAL30Q_BM25.res", "data/runs2017_table3/UOS-test")
copy("data/tar-master/2017-TAR/participant-runs/UOS/test/sis.TMBEST_BM25.res", "data/runs2017_table3/UOS-test")


os.mkdir("data/runs2017_table3/Waterloo/")
copy("data/tar-master/2017-TAR/participant-runs/Waterloo/A-rank-normal.txt", "data/runs2017_table3/Waterloo")
copy("data/tar-master/2017-TAR/participant-runs/Waterloo/B-rank-normal.txt", "data/runs2017_table3/Waterloo")


os.mkdir("data/runs2017_table3/Baseline/")
copy("data/tar-master/2017-TAR/participant-runs/UOS/test/pubmed.random.res", "data/runs2017_table3/Baseline")
copy("data/tar-master/2017-TAR/participant-runs/UOS/test/sis.BM25.res", "data/runs2017_table3/Baseline")
os.rename("data/runs2017_table3/Baseline/sis.BM25.res", "data/runs2017_table3/Baseline/BM25.res") # to match AURC name

# PRINT RESULTS
all_runs = glob.glob('data/runs2017_table3/*/*')
print("Number runs:", len(all_runs))

for run in all_runs:
    print(run)