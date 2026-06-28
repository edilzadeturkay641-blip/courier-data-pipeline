import pandas as pd
from db import get_engine
    
df = pd.read_json("data/companies.json")

engine = get_engine()

df.to_sql(
    "company",
    con=engine,
    if_exists="replace",
    index=False
)

print("Companies table created successfully!  load_customers.py:15 - load_companies.py:15")
print(df.head())