import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from config import POSTGRES_URL

wr_file = 'others/swimming_wr.xlsx'
df = pd.read_excel(wr_file)

def sqlite():
    with sqlite3.connect('masters.db') as conn:
        df.to_sql('world_records', conn, if_exists='replace', index=False)

def postgresql():
    engine = create_engine(POSTGRES_URL)
    df.to_sql('world_records', engine, if_exists='append', index=False)

def add_cor():
    df_cor = pd.read_excel('splash_files\cor.xlsx')
    engine = create_engine(POSTGRES_URL)
    df_cor.to_sql('results', engine, if_exists='append', index=False)

add_cor()