import pandas as pd
import os

def create_full_df():
    full_df = pd.DataFrame(columns = ["Summary"])
    directory = os.getcwd()
    for filename in os.listdir(directory + "\\data\\"):
        new_df = pd.read_csv("data//" + filename)
        full_df = pd.concat([full_df, new_df], ignore_index=True, axis=0)
    return full_df.drop_duplicates()  

def full_df_to_text_data(full_df):
    text_data = "" 
    for data in full_df["Summary"]:
        text_data += data
    return text_data    

textfile = open('text_data.txt', 'w', encoding="utf-8")
textfile.write(full_df_to_text_data(create_full_df()))
textfile.close()
