import pandas as pd
from db import get_engine
    
df = pd.read_csv("data/orders.csv")

engine = get_engine()

df.to_sql(
    "orders",
    con=engine,
    if_exists="replace",
    index=False
)

print("Orders table created successfully!  load_customers.py:15 - load_orders.py:15")
print(df.head())