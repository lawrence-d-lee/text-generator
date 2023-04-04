import pandas as pd
import os

def create_full_df():
    full_df = pd.DataFrame(columns = ["Summary"])
    directory = os.getcwd()
    for filename in os.listdir(directory + "\\data\\"):
        new_df = pd.read_csv("data//" + filename)
        full_df = pd.concat([full_df, new_df], ignore_index=True, axis=0)
    return full_df.drop_duplicates()  

full_df = create_full_df()
full_df.to_csv('all_sentences', index=False)