import pandas as pd
import random
from datetime import datetime, timedelta

cities = [
    "Baku",
    "Ganja",
    "Sumgait",
    "Mingachevir",
    "Shaki",
    "Lankaran"
]

statuses = [
    "delivered",
    "cancelled",
    "failed",
    "returned"
]

orders = []

for i in range(1, 10001):

    orders.append({
        "order_id": i,
        "customer_id": random.randint(1, 1000),
        "company_id": random.randint(1, 20),
        "city": random.choice(cities),
        "amount": round(random.uniform(5, 300), 2),

        "order_date": (
            datetime(2025, 1, 1)
            + timedelta(days=random.randint(0, 365))
        ).strftime("%Y-%m-%d"),

        "status": random.choice(statuses)
    })

df = pd.DataFrame(orders)

df.to_csv(
    "data/orders.csv",
    index=False
)

print("10000 orders generated - generate_orders.py:47")