import pandas as pd
import plotly.express as px
import streamlit as st


def sales_trend(df: pd.DataFrame, date_col: str = 'order_placed_at') -> None:
    trend = (
        df.assign(_date=pd.to_datetime(df[date_col]).dt.date)
        .groupby('_date', as_index=False)['order_amount']
        .sum()
        .rename(columns={'_date': 'date', 'order_amount': 'total_sales'})
    )
    fig = px.line(trend, x='date', y='total_sales', markers=True, title='Sales Trend')
    fig.update_layout(yaxis_title='Total Sales (INR)', xaxis_title='Date')
    st.plotly_chart(fig, width='stretch')


def top_n_bar(df: pd.DataFrame, category: str, value: str, title: str, n: int = 10) -> None:
    grouped = (
        df.groupby(category, as_index=False)[value]
        .sum()
        .sort_values(value, ascending=False)
        .head(n)
    )
    fig = px.bar(grouped, x=value, y=category, orientation='h', title=title, text_auto='.2s')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, width='stretch')
