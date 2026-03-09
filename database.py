import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine("postgresql://postgres:Aditya%40123@localhost:5432/gc_data")

csv_folder = "./data"

for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        table_name = file.replace(".csv", "").lower() 
        df = pd.read_csv(f"{csv_folder}/{file}")
        
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )
    