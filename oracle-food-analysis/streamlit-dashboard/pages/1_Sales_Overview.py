import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.charts import sales_trend, top_n_bar
from lib.db import run_query
from lib.filters import apply_global_filters
from lib.metrics import render_kpis

st.set_page_config(page_title='Sales Overview', page_icon='??', layout='wide')
st.title('Sales Overview')

@st.cache_data(ttl=300, show_spinner=False)
def load_orders():
    return run_query('''
        SELECT
            o.order_id,
            o.order_placed_at,
            o.status,
            o.partner,
            o.order_amount,
            o.customer_id,
            c.customer_name,
            c.city,
            c.area
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
    ''')

df = load_orders()
filtered = apply_global_filters(df, date_col='order_placed_at')

render_kpis(filtered)

left, right = st.columns(2)
with left:
    sales_trend(filtered)
with right:
    top_n_bar(filtered, category='customer_name', value='order_amount', title='Top 10 Customers by Sales')

top_n_bar(filtered, category='area', value='order_amount', title='Top 10 Areas by Sales')

st.subheader('Pivot Table: Sales by Area and Status')
pivot = pd.pivot_table(
    filtered,
    index='area',
    columns='status',
    values='order_amount',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total',
)
st.dataframe(pivot, use_container_width=True)

with st.expander('View filtered data'):
    st.dataframe(filtered, use_container_width=True)
