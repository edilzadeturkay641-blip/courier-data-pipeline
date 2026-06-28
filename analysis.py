import pandas as pd
from db import get_engine

engine = get_engine()

customers = pd.read_sql(
    "SELECT * FROM customers",
    con=engine
)

print(1)

orders = pd.read_sql(
    "SELECT * FROM orders",
    con=engine
)


deliveries = pd.read_sql(
        "SELECT * FROM deliveries",
        con=engine
)


