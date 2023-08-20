import pandas as pd

def clean_data(df):


    df.columns = df.columns.str.replace(' ', '_').str.strip().str.lower()

    return df