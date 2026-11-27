import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(page_title='Food Analysis Dashboard', page_icon='📊', layout='wide')

page = st.sidebar.radio('Dashboard', ['Sales Overview', 'Customer Map'])

if page == 'Sales Overview':
    from views.sales_overview import render
    render()
else:
    from views.customer_map import render
    render()
