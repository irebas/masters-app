import sqlite3
import pandas as pd

def main():
    wr_file = 'swimming_wr.xlsx'
    df = pd.read_excel(wr_file)
    print(df)
    with sqlite3.connect('masters.db') as conn:
        df.to_sql('world_records', conn, if_exists='replace', index=False)

main()
