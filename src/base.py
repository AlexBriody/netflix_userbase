from cleaning_data import clean_data
import pandas as pd

class Base:
    def __init__(self):
        self.df = None
        
    def clean_and_process_data(self, filepath):
        df = pd.read_csv(filepath)
        self.df = clean_data(df)

if __name__ == '__main__':
    c = Base()
    c.clean_and_process_data('netflix_database.csv')
    
    if c.df is not None:
        c.df.to_csv('data/oracle_cards.csv', index=False)
    else:
        print("DataFrame is None")