# Streamlit Dashboard (Scalable Starter)

This folder contains a modular Streamlit app for Oracle `FOOD_ANALYSIS` dashboards.

## Structure

```text
streamlit-dashboard/
  Home.py                 # Home / entry point
  views/                  # Add one file per dashboard page
    sales_overview.py
    customer_map.py
  lib/
    db.py                 # Oracle engine + cached query helper
    filters.py            # Reusable global filters at the top of each page
    metrics.py            # KPI cards
    charts.py             # Reusable chart components
```

## Run

From the repository root:

```powershell
uv sync
uv run poe oracle-up
uv run poe dashboard
```

Equivalent commands:

```powershell
docker compose --env-file .env -f oracle-food-analysis/docker-compose.yml up -d
uv run streamlit run oracle-food-analysis/streamlit-dashboard/Home.py
```

## Add a new dashboard

1. Create `views/3_My_Dashboard.py`.
2. Query data with `lib.db.run_query`.
3. Apply shared filters with `lib.filters.apply_global_filters`.
4. Reuse KPI/chart helpers or add new helpers in `lib/`.
5. For heavy/official metrics, prefer Oracle views (like `VW_TOP_10_*`) and query them from the dashboard.

## Design notes

- Keep SQL in views or dedicated query functions for reuse.
- Cache expensive queries with `st.cache_data(ttl=...)`.
- Cache the DB engine with `st.cache_resource`.
- Keep filters consistent across pages (date, city, area, status).
- The Customer Map uses GeoPandas/Matplotlib; Sales Overview charts continue to use Plotly.
- Define metric logic once (e.g., sales = `SUM(order_amount)`, exclude cancelled?).


