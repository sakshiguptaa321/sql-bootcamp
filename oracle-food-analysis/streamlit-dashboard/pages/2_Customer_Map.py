import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.db import run_query

st.set_page_config(page_title='Customer Map', page_icon='???', layout='wide')
st.title('Customer Area Sales Map')

@st.cache_data(ttl=300, show_spinner=False)
def load_area_sales():
    return run_query('''
        SELECT
            c.area,
            c.city,
            COUNT(DISTINCT c.customer_id) AS total_customers,
            COUNT(o.order_id) AS total_orders,
            SUM(o.order_amount) AS total_sales
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.area, c.city
    ''')

coords = pd.DataFrame([
    {'area': 'Whitefield', 'lat': 12.9698, 'lon': 77.7499},
    {'area': 'HSR Layout', 'lat': 12.9121, 'lon': 77.6446},
    {'area': 'Bellandur', 'lat': 12.9260, 'lon': 77.6762},
    {'area': 'Electronic City', 'lat': 12.8399, 'lon': 77.6770},
    {'area': 'BTM Layout', 'lat': 12.9166, 'lon': 77.6101},
    {'area': 'Koramangala', 'lat': 12.9352, 'lon': 77.6245},
    {'area': 'Indiranagar', 'lat': 12.9719, 'lon': 77.6412},
    {'area': 'JP Nagar', 'lat': 12.9063, 'lon': 77.5857},
    {'area': 'Rajajinagar', 'lat': 12.9982, 'lon': 77.5530},
    {'area': 'Jayanagar', 'lat': 12.9308, 'lon': 77.5838},
    {'area': 'Marathahalli', 'lat': 12.9591, 'lon': 77.6974},
    {'area': 'Malleshwaram', 'lat': 13.0031, 'lon': 77.5643},
])

df = load_area_sales().merge(coords, on='area', how='left')

def sales_threshold(amount):
    if amount >= 25000:
        return 'High (>= 25,000)'
    if amount >= 15000:
        return 'Medium (15,000 - 24,999)'
    return 'Low (< 15,000)'

df['sales_band'] = df['total_sales'].apply(sales_threshold)

fig = px.scatter_map(
    df,
    lat='lat',
    lon='lon',
    size='total_sales',
    color='sales_band',
    hover_name='area',
    hover_data={'total_sales': ':,.0f', 'total_orders': True, 'total_customers': True, 'lat': False, 'lon': False},
    color_discrete_map={
        'High (>= 25,000)': '#d73027',
        'Medium (15,000 - 24,999)': '#fee08b',
        'Low (< 15,000)': '#4575b4',
    },
    zoom=11,
    height=650,
    title='Bangalore Area Sales Map',
)
fig.update_layout(map_style='carto-positron', margin={'r': 0, 't': 40, 'l': 0, 'b': 0})
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df[['area', 'city', 'total_customers', 'total_orders', 'total_sales', 'sales_band']].sort_values('total_sales', ascending=False), use_container_width=True)

