This repository contains code to run algorithms for the Poisson process, target method and knee method for determining stopping points as described in our EMNLP 2019 paper "Modelling Stopping Criteria for Search Results using Poisson Processes" https://arxiv.org/abs/1909.06239.

The main results in the paper can be replicated by downloading a copy of the 2017 CLEF TAR data (available at https://github.com/CLEF-TAR/tar) into the repository's data folder and running (in order): 

python process_data.py

python run_stopping_point_algorithms.py

python analyse_results.py

