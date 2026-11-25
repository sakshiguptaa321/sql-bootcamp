import pandas as pd
import streamlit as st


def apply_global_filters(df: pd.DataFrame, date_col: str | None = None) -> pd.DataFrame:
    filtered = df.copy()

    st.sidebar.header('Global Filters')

    if 'city' in filtered.columns:
        cities = sorted([c for c in filtered['city'].dropna().unique()])
        selected_cities = st.sidebar.multiselect('City', cities, default=cities)
        if selected_cities:
            filtered = filtered[filtered['city'].isin(selected_cities)]

    if 'area' in filtered.columns:
        areas = sorted([a for a in filtered['area'].dropna().unique()])
        selected_areas = st.sidebar.multiselect('Area', areas, default=areas)
        if selected_areas:
            filtered = filtered[filtered['area'].isin(selected_areas)]

    if 'status' in filtered.columns:
        statuses = sorted([s for s in filtered['status'].dropna().unique()])
        selected_statuses = st.sidebar.multiselect('Order status', statuses, default=statuses)
        if selected_statuses:
            filtered = filtered[filtered['status'].isin(selected_statuses)]

    if date_col and date_col in filtered.columns:
        filtered[date_col] = pd.to_datetime(filtered[date_col])
        min_date = filtered[date_col].min().date()
        max_date = filtered[date_col].max().date()
        date_range = st.sidebar.date_input('Date range', value=(min_date, max_date), min_value=min_date, max_value=max_date)
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start, end = date_range
            mask = (filtered[date_col].dt.date >= start) & (filtered[date_col].dt.date <= end)
            filtered = filtered[mask]

    return filtered
