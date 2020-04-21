from flask import json
import pandas as pd
from application import Config, functions, modals
import os

def Global_EUC():
    query = "SELECT current_count, total_fn_count from script_progress WHERE script_id = ?"
    rv = modals.query_db(query, [1], one=True)
    if rv is None:
        insert_query = "INSERT INTO script_progress (script_id, current_count, total_fn_count) VALUES (?,?,?)"
        insert_args = (1,0,2)
        msg = modals.write_db(insert_query,insert_args,"added")
        print(msg)
    else:
        up_qry = "UPDATE script_progress SET current_count = ?, total_fn_count = ? WHERE script_id = ?"
        up_args = (0,2,1)
        msg = modals.write_db(up_qry, up_args,"updated")
        print(msg)

    

    df = pd.read_csv("/Users/sshankar7/OneDrive/Personal_Work/Zbay_Ecommerce-WNS_Analytics_Wizard/train.csv")
    
    print("DF Shape",df.shape)
    up_qry = "UPDATE script_progress SET current_count = ?, total_fn_count = ? WHERE script_id = ?"
    up_args = (1,2,1)
    msg = modals.write_db(up_qry, up_args,"updated")
    print(msg)
    
    """
    Code Segment for Global EUC 
    """
    df1 = pd.read_excel("/Users/sshankar7/OneDrive/Personal_Work/gtd/gtd_14to17_0718dist.xlsx")
    print("DF1 shape",df1.shape)
    up_qry = "UPDATE script_progress SET current_count = ?, total_fn_count = ? WHERE script_id = ?"
    up_args = (2,2,1)
    msg = modals.write_db(up_qry, up_args,"updated")
    print(msg)
    
