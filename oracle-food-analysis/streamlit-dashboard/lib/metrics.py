import pandas as pd
import streamlit as st


def render_kpis(df: pd.DataFrame) -> None:
    total_sales = float(df['order_amount'].sum()) if 'order_amount' in df else 0.0
    total_orders = int(df['order_id'].nunique()) if 'order_id' in df else len(df)
    avg_order_value = total_sales / total_orders if total_orders else 0.0
    active_customers = int(df['customer_id'].nunique()) if 'customer_id' in df else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Total Sales', f'INR {total_sales:,.0f}')
    c2.metric('Total Orders', f'{total_orders:,}')
    c3.metric('Avg Order Value', f'INR {avg_order_value:,.0f}')
    c4.metric('Active Customers', f'{active_customers:,}')
