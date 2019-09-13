# -*- coding: utf-8 -*-
"""
@author: Alison Sneyd

This script analyses the experiement results.
"""

# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# READ DATA
df = pd.read_csv("2017run_scores")
df = df.rename(columns={"Unnamed: 0": "Run"})
df_aur = pd.read_csv("data/runs2017_AURC.csv")
runs = df["Run"][:-1] # [:-1] = drop mean
aurc = df_aur["AURC"]

# GET RESULTS FOR TOP, MID AND BOTTOM 5 RUNS
sorted_idxs = [i for i in np.argsort(aurc)[::-1]]
top5idxs = sorted_idxs[0:5]
bottom5idxs = sorted_idxs[-5:]
mid5idxs = sorted_idxs[14:19]  # 15-19 inclusive

for i in top5idxs:
    print(runs[i])
print("\n")
for i in mid5idxs:
    print(runs[i])
print("\n")
for i in bottom5idxs:
    print(runs[i])
    
dftop5 = pd.DataFrame(columns=df.columns)
for i in top5idxs:
    dftop5 = dftop5.append(df.loc[i])
    
dfmid5 = pd.DataFrame(columns=df.columns)
for i in mid5idxs:
    dfmid5 = dfmid5.append(df.loc[i])
    
dfbottom5 = pd.DataFrame(columns=df.columns)
for i in bottom5idxs:
    dfbottom5 = dfbottom5.append(df.loc[i])
    
df_means = pd.DataFrame(columns=df.columns)
df_means = df_means.append(df.loc[33], ignore_index = True)
df_means = df_means.append(dftop5.mean(), ignore_index = True)
df_means = df_means.append(dfmid5.mean(), ignore_index = True)
df_means = df_means.append(dfbottom5.mean(), ignore_index = True)
df_means = df_means.round(2)
df_means = df_means.drop("Run", axis = 1)
df_means["Mean"] = ["All 33", "Top 5", "Mid 5", "Bottom 5"]
df_means = df_means.set_index('Mean')

df_means = df_means.rename({'tar tot eff': 'TM', 
                            'kn150 tot eff': 'KM-default',
                            'kn50 tot eff': 'KM-tuned', 
                            'in tot eff': 'PP','oracle eff': 'OR'}, axis=1)
print(df_means)


# PROCESS DATA INTO LATEX TABLE
df_latex = df_means.T
df_latex = df_latex.tail(5)
df_latex = df_latex.round()
df_latex = df_latex.astype('int32')

def pes(eff):  # fn to calculate % of effort saved
    saving = 117562-eff
    return round(100*saving/117562,1)

df_latex_p1 = df_latex[["All 33"]].copy()
All33 = df_latex_p1["All 33"].tolist()
df_latex_p1["ALL 33 ES"] = [pes(eff) for eff in All33]
df_latex_p2 = df_latex[["Top 5"]].copy()
Top5 = df_latex_p2["Top 5"].tolist()
df_latex_p2["Top5 ES"]= [pes(eff) for eff in Top5]
df_latex_p3 = df_latex[["Mid 5"]].copy()
Mid5 = df_latex_p3["Mid 5"].tolist()
df_latex_p3["Mid 5 ES"] = [pes(eff) for eff in Mid5]
df_latex_p4 = df_latex[["Bottom 5"]].copy()
Bottom5 = df_latex_p4["Bottom 5"].tolist()
df_latex_p4["Bottom ES"] = [pes(eff) for eff in Bottom5]

print(df_latex_p1.to_latex())
print(df_latex_p2.to_latex())
print(df_latex_p3.to_latex())
print(df_latex_p4.to_latex())



# MAKE ORACLE AND PP EFFORT GRAPH
oracle = df["oracle eff"].tolist()[:-1]
in_eff = df["in tot eff"].tolist()[:-1]
sorted_oracle = [oracle[i] for i in sorted_idxs]
sorted_in_eff = [in_eff[i] for i in sorted_idxs]
sorted_aur = [aurc[i] for i in sorted_idxs]

plt.figure()
plt.plot(sorted_aur, sorted_in_eff, linestyle='-',marker='.',
                        label = "PP effort")
plt.plot(sorted_aur, sorted_oracle, linestyle='-',marker='x',
                        label = "Oracle effort")
plt.ylabel("Total Effort")
plt.xlabel("AURC")
plt.legend()
plt.savefig("Effort_graph.png")