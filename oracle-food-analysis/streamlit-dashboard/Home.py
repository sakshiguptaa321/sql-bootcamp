import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(page_title='Food Analysis Dashboard', page_icon='??', layout='wide')

st.title('Food Analysis Dashboard')
st.write(
    '''
This Streamlit app provides a scalable starting point for Oracle `FOOD_ANALYSIS` dashboards.

Use the pages in the sidebar for:
- **Sales Overview**: global filters, KPIs, trend, top customers/cities, and pivot table.
- **Customer Map**: area-level sales map with threshold colors.

### How to add a new dashboard
1. Create a new file in `pages/`, e.g. `3_Product_Performance.py`.
2. Reuse shared helpers from `lib/` (`db.run_query`, `filters.apply_global_filters`, `metrics.render_kpis`).
3. Add SQL/views for trusted metrics when the dashboard grows.
'''
)
