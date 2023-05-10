"""
Module defining the Examination class
"""
import sqlite3
import pandas as pd

class Examination():
    """
    Class Examination holds every information about all kind of competitor's 
    tests results and data.
    """
    def __init__(self, searching_key: str="competitor_id", searchig_value: any=1):
        self.get_values_form_db(searching_key, searchig_value)
        self.RR_yoyo = pd.read_csv(self.examination_path, sep="\t", index_col=None, header=2)
        print(self.RR_yoyo)
    
    def get_values_form_db(self, searching_key, searchig_value):
        conn = sqlite3.connect('yoyo.db')  
        res = pd.read_sql_query(f"SELECT * FROM Competitors WHERE {searching_key} = {searchig_value}", conn)
        self.examination_path = res['examination_path'].tolist()[0]

if __name__ == "__main__":
    ex = Examination()