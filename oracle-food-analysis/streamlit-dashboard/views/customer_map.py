import sys
from pathlib import Path

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.db import run_query


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


def sales_threshold(amount):
    if amount >= 25000:
        return 'High (>= 25,000)'
    if amount >= 15000:
        return 'Medium (15,000 - 24,999)'
    return 'Low (< 15,000)'


def render():
    st.title('Customer Area Sales Map')

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
    df['sales_band'] = df['total_sales'].apply(sales_threshold)

    color_map = {
        'High (>= 25,000)': '#d73027',
        'Medium (15,000 - 24,999)': '#fee08b',
        'Low (< 15,000)': '#4575b4',
    }

    gdf = gpd.GeoDataFrame(
        df.dropna(subset=['lat', 'lon']),
        geometry=[Point(xy) for xy in zip(df.dropna(subset=['lat', 'lon'])['lon'], df.dropna(subset=['lat', 'lon'])['lat'])],
        crs='EPSG:4326',
    ).to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(12, 10))
    for band, color in color_map.items():
        subset = gdf[gdf['sales_band'] == band]
        if not subset.empty:
            subset.plot(
                ax=ax,
                color=color,
                markersize=subset['total_sales'] / 80,
                alpha=0.75,
                edgecolor='black',
                linewidth=0.6,
                label=band,
                zorder=3,
            )

    for _, row in gdf.iterrows():
        ax.annotate(
            text=row['area'],
            xy=(row.geometry.x, row.geometry.y),
            xytext=(3, 3),
            textcoords='offset points',
            fontsize=8,
        )

    try:
        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldStreetMap)
    except Exception as exc:
        st.warning(f'Basemap tiles could not be loaded ({exc}). Showing points without basemap.')

    ax.set_axis_off()
    ax.set_title('Bangalore Customer Sales by Area', fontsize=14)
    ax.legend(title='Sales Threshold', loc='lower left')
    st.pyplot(fig, width='stretch')
    plt.close(fig)

    st.dataframe(
        df[['area', 'city', 'total_customers', 'total_orders', 'total_sales', 'sales_band']].sort_values('total_sales', ascending=False),
        width='stretch',
    )
