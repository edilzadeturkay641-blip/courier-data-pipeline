import pandas as pd
from db import get_engine

df = pd.read_json("data/customers.json")

engine = get_engine()

df.to_sql(
    "customers",
    con=engine,
    if_exists="replace",
    index=False
)

print("Customers table created successfully! - load_customers.py:15")
print(df.head())