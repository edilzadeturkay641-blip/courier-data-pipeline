from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime
import pandas as pd
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_DIR))

from db import get_engine

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

#------ orders by city


def orders_by_city_etl():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = get_engine()

    orders = pd.read_sql("SELECT * FROM orders", con=engine)

    orders = orders.dropna(subset=["city"])
    orders = orders[orders["city"].str.strip() != ""]

    orders_by_city = (
        orders
        .groupby("city")
        .size()
        .reset_index(name="total_orders")
        .sort_values("total_orders", ascending=False)
    )

    orders_by_city.to_csv(
        OUTPUT_DIR / "orders_by_city.csv",
        index=False
    )

    pd.DataFrame({
        "total_orders": [len(orders)]
    }).to_csv(
        OUTPUT_DIR / "total_orders.csv",
        index=False
    )

#------ orders by company
def revenue_by_company_etl():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = get_engine()

    orders = pd.read_sql("SELECT * FROM orders", con=engine)
    companies = pd.read_sql("SELECT * FROM company", con=engine)

    orders_companies = orders.merge(
        companies,
        on="company_id",
        how="left"
    )

    orders_companies = orders_companies.dropna(
        subset=["company_name", "amount"]
    )

    revenue_by_company = (
        orders_companies
        .groupby("company_name")["amount"]
        .sum()
        .reset_index(name="total_revenue")
        .sort_values("total_revenue", ascending=False)
    )

    revenue_by_company.to_csv(
        OUTPUT_DIR / "revenue_by_company.csv",
        index=False
    )



#------delivery status

def delivery_status_etl():  
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = get_engine()

    deliveries = pd.read_sql("SELECT * FROM deliveries", con=engine)

    deliveries = deliveries.dropna(subset=["delivery_status"])

    delivery_status = (
        deliveries
        .groupby("delivery_status")
        .size()
        .reset_index(name="total_deliveries")
    )

    status_order = ["Delivered", "Failed", "Cancelled"]

    delivery_status["delivery_status"] = pd.Categorical(
        delivery_status["delivery_status"],
        categories=status_order,
        ordered=True
    )

    delivery_status = delivery_status.sort_values("delivery_status")

    delivery_status.to_csv(
        OUTPUT_DIR / "delivery_status.csv",
        index=False
    )

    total_deliveries = delivery_status["total_deliveries"].sum()

    pd.DataFrame({
        "total_deliveries": [total_deliveries]
    }).to_csv(
        OUTPUT_DIR / "total_deliveries.csv",
        index=False
    )

    failed_count = delivery_status.loc[
        delivery_status["delivery_status"] == "Failed",
        "total_deliveries"
    ].sum()

    failed_rate = (
        failed_count / total_deliveries * 100
        if total_deliveries > 0
        else 0
    )

    pd.DataFrame({
        "failed_rate": [failed_rate]
    }).to_csv(
        OUTPUT_DIR / "failed_rate.csv",
        index=False
    )

#------ orders by months


def monthly_orders_etl():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = get_engine()

    orders = pd.read_sql(
        "SELECT * FROM orders",
        con=engine
    )

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    monthly_orders = (
        orders
        .dropna(subset=["order_date"])
        .assign(month=lambda x: x["order_date"].dt.strftime("%b %Y"))
        .groupby("month")
        .size()
        .reset_index(name="total_orders")
    )

    month_order = [
        "Jan 2025", "Feb 2025", "Mar 2025", "Apr 2025",
        "May 2025", "Jun 2025", "Jul 2025", "Aug 2025",
        "Sep 2025", "Oct 2025", "Nov 2025", "Dec 2025",
        "Jan 2026"
    ]

    monthly_orders["month"] = pd.Categorical(
        monthly_orders["month"],
        categories=month_order,
        ordered=True
    )

    monthly_orders = monthly_orders.sort_values("month")

    monthly_orders.to_csv(
        OUTPUT_DIR / "monthly_orders.csv",
        index=False
    )



#---------weather impact




def weather_monthly_etl():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = get_engine()

    orders = pd.read_sql(
        "SELECT * FROM orders",
        con=engine
    )

    deliveries = pd.read_sql(
        "SELECT * FROM deliveries",
        con=engine
    )

    weather = pd.read_sql(
        "SELECT * FROM weather",
        con=engine
    )

    weather["weather_date"] = pd.to_datetime(
        weather["weather_date"],
        errors="coerce"
    )

    deliveries["delivery_date"] = pd.to_datetime(
        deliveries["delivery_date"],
        errors="coerce"
    )

    weather_delivery = (
        deliveries
        .merge(
            orders[["order_id", "city"]],
            on="order_id",
            how="left"
        )
        .merge(
            weather,
            left_on=["city", "delivery_date"],
            right_on=["city", "weather_date"],
            how="left"
        )
    )

    weather_delivery = weather_delivery.dropna(
        subset=[
            "delivery_duration_minutes",
            "temperature",
            "rain",
            "wind_speed"
        ]
    )

    weather_delivery["month"] = (
        weather_delivery["delivery_date"]
        .dt.to_period("M")
        .dt.strftime("%b %Y")
    )

    weather_delivery["month_order"] = (
        weather_delivery["delivery_date"]
        .dt.to_period("M")
        .astype(str)
    )

    weather_monthly = (
        weather_delivery
        .groupby(["month_order", "month"])
        .agg(
            avg_delivery_time=("delivery_duration_minutes", "mean"),
            avg_temperature=("temperature", "mean"),
            avg_rain=("rain", "mean"),
            avg_wind=("wind_speed", "mean")
        )
        .reset_index()
        .sort_values("month_order")
    )

    weather_monthly.to_csv(
        OUTPUT_DIR / "weather_monthly.csv",
        index=False
    )   


    # DAG 

with DAG(
    dag_id="orders_city_etl",
    start_date=datetime(2026, 6, 28),
    schedule="@daily",
    catchup=False
) as dag:

    task_orders_by_city = PythonOperator(
        task_id="orders_by_city",
        python_callable=orders_by_city_etl
    )

    task_revenue_by_company = PythonOperator(
        task_id="revenue_by_company",
        python_callable=revenue_by_company_etl
    )

    task_delivery_status = PythonOperator(
        task_id="delivery_status",
        python_callable=delivery_status_etl
    )

    task_monthly_orders = PythonOperator(
        task_id="monthly_orders",
        python_callable=monthly_orders_etl
    )
    task_weather_monthly = PythonOperator(
    task_id="weather_monthly",
    python_callable=weather_monthly_etl
    )


    task_orders_by_city >> task_revenue_by_company >> task_delivery_status >> task_monthly_orders >> task_weather_monthly