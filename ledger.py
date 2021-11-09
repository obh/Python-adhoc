#!/bin/python

import pandas as pd
import numpy as np

#df = pd.read_csv("/tmp/g")
df = pd.read_csv("~/Downloads/ledger.csv")
df = df.sort_values(['id'], ascending=[False])
main_s = list(range(len(df)))
df = df.set_index( [main_s] )

midlist = list(np.unique(df["merchantid"].values))
#midlist = [1]
for mid in midlist:
    mid_df = df[df["merchantid"] == mid]
    _open = mid_df["closingbalance"].copy(deep=True).to_frame()
    
    series = list(range(len(mid_df)))
    
    mid_df = mid_df.set_index([series])
    _open = _open.set_index([series])
    
    _open = _open[1:]
    _open.loc[len(mid_df)] = 0
    _open = _open.rename(columns={'closingbalance' : 'openingbalance'})
    
    mid_df = mid_df.set_index([series])
    _open = _open.set_index([series])
    join = mid_df.join(_open)
    join["multiply"] = join["saletype"].apply(lambda x: -1 if x == 'DEBIT' else 1)
    
    join["diff"] = join["multiply"] * join["amount"] + join["openingbalance"] - join["closingbalance"]
    impacted = len(join[ (join["diff"] < 0 | (join["diff"] > 0)) & (join["openingbalance"] > 0) ])
    #if impacted > 0:    
    print(mid, impacted)
    #print(join)


