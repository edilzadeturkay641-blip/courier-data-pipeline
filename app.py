import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

import plotly.graph_objects as go


st.set_page_config(
    page_title="Courier Company Dashboard",
    layout="wide"
)

DATA_DIR = Path("data/processed")

orders_by_city_file = DATA_DIR / "orders_by_city.csv"
total_orders_file = DATA_DIR / "total_orders.csv"

if not orders_by_city_file.exists() or not total_orders_file.exists():
    st.warning("Əvvəl Airflow-da orders_city_etl DAG-ını işə sal.")
    st.stop()

orders_by_city = pd.read_csv(orders_by_city_file)
total_orders = pd.read_csv(total_orders_file)["total_orders"][0]

st.title("Courier Company Dashboard")

st.metric(
    label="Total Orders",
    value=f"{total_orders:,}"
)

st.divider()

fig = px.bar(
    orders_by_city,
    x="total_orders",
    y="city",
    orientation="h",
    text="total_orders",
    color="total_orders",
    color_continuous_scale="Blues"
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    title="Orders by City",
    xaxis_title="Total Orders",
    yaxis_title="",
    coloraxis_showscale=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=550,
    font=dict(size=14),
    yaxis=dict(
        autorange="reversed"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)




# ================= REVENUE BY COMPANY =================

revenue_by_company_file = DATA_DIR / "revenue_by_company.csv"

if not revenue_by_company_file.exists():
    st.warning("Əvvəl Airflow-da revenue_by_company task-ını işə sal.")
    st.stop()

revenue_by_company = pd.read_csv(revenue_by_company_file)

total_revenue = revenue_by_company["total_revenue"].sum()

st.subheader("Revenue by Company")

st.metric(
    label="Total Revenue",
    value=f"{total_revenue:,.2f} AZN"
)

fig2 = px.pie(
    revenue_by_company,
    names="company_name",
    values="total_revenue",
    hole=0.60,
    color="company_name",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

fig2.update_traces(
    textinfo="label+percent",
    textposition="inside",
    insidetextorientation="horizontal",
    hovertemplate=
    "<b>%{label}</b><br>"
    "Revenue: %{value:,.2f} AZN<br>"
    "Share: %{percent}<extra></extra>"
)

fig2.update_layout(
    title="Revenue Share by Company",
    title_x=0.02,
    height=650,
    showlegend=True,
    legend_title="Companies",
    font=dict(size=14),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
# ================= DELIVERY STATUS =================

delivery_status_file = DATA_DIR / "delivery_status.csv"
total_deliveries_file = DATA_DIR / "total_deliveries.csv"
failed_rate_file = DATA_DIR / "failed_rate.csv"

if (
    not delivery_status_file.exists()
    or not total_deliveries_file.exists()
    or not failed_rate_file.exists()
):
    st.warning("Əvvəl Airflow-da delivery_status task-ını işə sal.")
    st.stop()

delivery_status = pd.read_csv(delivery_status_file)
total_deliveries = pd.read_csv(total_deliveries_file)["total_deliveries"][0]
failed_rate = pd.read_csv(failed_rate_file)["failed_rate"][0]

st.subheader("Delivery Status Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Total Deliveries",
        value=f"{total_deliveries:,}"
    )

with col2:
    st.metric(
        label="Failed Delivery Rate",
        value=f"{failed_rate:.2f}%"
    )

fig3 = px.funnel(
    delivery_status,
    x="total_deliveries",
    y="delivery_status",
    title="Delivery Status Funnel",
    color="delivery_status",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

fig3.update_traces(
    textinfo="value+percent initial"
)

fig3.update_layout(
    height=500,
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Total Deliveries",
    yaxis_title="Delivery Status",
    showlegend=False,
    font=dict(size=14),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ================= MONTHLY ORDERS TREND =================

monthly_orders_file = DATA_DIR / "monthly_orders.csv"

if not monthly_orders_file.exists():
    st.warning("Əvvəl Airflow-da monthly_orders ETL-ni işə sal.")
    st.stop()

monthly_orders = pd.read_csv(monthly_orders_file)

st.subheader("Monthly Orders Trend")

fig4 = px.line(
    monthly_orders,
    x="month",
    y="total_orders",
    text="total_orders",
    markers=True
)

fig4.update_traces(
    mode="lines+markers+text",
    textposition="top center",
    line_shape="linear",
    line=dict(
        color="#1565C0",
        width=3
    ),
    marker=dict(
        size=9,
        color="#1565C0"
    ),
    textfont=dict(
        size=13,
        color="#1565C0"
    )
)

fig4.update_layout(
    title="Monthly Orders Trend",
    template="plotly_white",
    height=500,
    showlegend=False,
    xaxis_title="Month",
    yaxis_title="Total Orders",
    hovermode="x unified"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)



# ================= weather impact  =================

weather_monthly_file = DATA_DIR / "weather_monthly.csv"

if not weather_monthly_file.exists():
    st.warning("Əvvəl Airflow-da weather_monthly ETL-ni işə sal.")
    st.stop()

weather_monthly = pd.read_csv(weather_monthly_file)

st.subheader("Weather Impact on Delivery")

fig_weather = go.Figure()

fig_weather.add_trace(
    go.Bar(
        x=weather_monthly["month"],
        y=weather_monthly["avg_rain"],
        name="Rain (mm)",
        yaxis="y2",
        marker_color="#BBDEFB",
        opacity=0.65,
        text=weather_monthly["avg_rain"].round(1),
        textposition="outside"
    )
)

fig_weather.add_trace(
    go.Scatter(
        x=weather_monthly["month"],
        y=weather_monthly["avg_delivery_time"],
        mode="lines+markers+text",
        name="Delivery Time (min)",
        text=weather_monthly["avg_delivery_time"].round(1),
        textposition="top center",
        line=dict(color="#0D47A1", width=4),
        marker=dict(size=9, color="#0D47A1")
    )
)

fig_weather.add_trace(
    go.Scatter(
        x=weather_monthly["month"],
        y=weather_monthly["avg_temperature"],
        mode="lines+markers+text",
        name="Temperature (°C)",
        yaxis="y2",
        text=weather_monthly["avg_temperature"].round(1),
        textposition="top center",
        line=dict(color="#1976D2", width=3),
        marker=dict(size=7, color="#1976D2")
    )
)

fig_weather.add_trace(
    go.Scatter(
        x=weather_monthly["month"],
        y=weather_monthly["avg_wind"],
        mode="lines+markers+text",
        name="Wind Speed (km/h)",
        yaxis="y2",
        text=weather_monthly["avg_wind"].round(1),
        textposition="bottom center",
        line=dict(color="#64B5F6", width=3),
        marker=dict(size=7, color="#64B5F6")
    )
)

fig_weather.update_layout(
    title="Monthly Weather Impact on Delivery Performance",
    template="plotly_white",
    height=650,
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Average Delivery Time (Minutes)",
    yaxis2=dict(
        title="Weather Metrics",
        overlaying="y",
        side="right"
    ),
    legend=dict(
        orientation="h",
        y=1.03,
        x=0.5,
        xanchor="center"
    )
)

st.plotly_chart(
    fig_weather,
    use_container_width=True
)