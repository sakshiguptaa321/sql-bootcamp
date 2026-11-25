# Visualization Guide for Data Analysts

This folder contains Python notebooks that connect to the Oracle `FOOD_ANALYSIS` database and visualize reporting data with pandas, matplotlib, GeoPandas, and contextily.

## Notebooks

| Notebook | Purpose |
| --- | --- |
| `sales_visualization.ipynb` | Top 10 customers and top 10 cities by sales |
| `bangalore_map_visualization.ipynb` | Area-wise sales on a Bangalore basemap with threshold colors |
| `visualization_guide.ipynb` | Demo of common chart types and when to use them |

## Which chart to use where

| Business question / report type | Recommended chart | Why | Example in this dataset |
| --- | --- | --- | --- |
| Compare values across categories | Bar / horizontal bar chart | Easy to compare magnitudes across categories | Top 10 customers by sales, sales by city |
| Show trend over time | Line chart | Highlights direction, seasonality, and changes over time | Daily/monthly orders or sales trend |
| Show composition / share of total | Stacked bar / 100% stacked bar | Better than pie when there are many categories or precise comparison matters | Sales share by product category per city |
| Show part-to-whole for few categories | Donut / pie chart (use sparingly) | Quick high-level share view; avoid when >5 categories | Payment/partner share, delivered vs cancelled |
| Show distribution / spread | Histogram / box plot | Reveals skew, outliers, and spread | Order amount distribution, delivery/value spread |
| Show relationship between two numeric variables | Scatter plot | Shows correlation, clusters, and outliers | Quantity vs line amount, discount vs sales |
| Show relationship across many variables | Heatmap / correlation matrix | Good for density or matrix-style comparisons | Sales by area and category, correlation matrix |
| Show ranking with context | Sorted bar + labels | Makes rank and magnitude clear | Top customers, top products |
| Show geographic pattern | Map (bubble/choropleth) | Adds location context that tables/charts miss | Bangalore area sales map |
| Show KPI summary | KPI cards / single-value table | Fast executive view; pair with trend for context | Total sales, orders, AOV, active customers |

## Practical guidance

- **Start with the question, not the chart.** Ask: comparison, trend, composition, distribution, relationship, or geography?
- **Prefer bar charts for comparisons.** They are easier to read than pies for most business reports.
- **Use line charts only for ordered/time data.** Don't use lines for unordered categories.
- **Limit categories.** For top-N reports, show top 10 and group the rest as "Others" if needed.
- **Label clearly.** Include axis labels, units (?, count, %), and readable titles.
- **Use color with purpose.** Use thresholds/highlights to draw attention; avoid too many colors.
- **Avoid misleading axes.** For bar charts, start at zero unless there is a strong reason not to.
- **Use maps when location matters.** If location is not important, a bar chart is usually clearer.

## Suggested next steps

1. **Build a reporting notebook set** by report type: executive KPI, sales trend, customer ranking, product/category mix, geography.
2. **Create reusable chart functions** (e.g., `plot_top_n_bar`, `plot_trend_line`, `plot_sales_map`) to keep notebooks consistent.
3. **Add business filters**: date range, city, area, product category, order status.
4. **Validate metrics** before visualizing: define sales as `SUM(order_amount)` or `SUM(line_amount)`, decide whether cancelled orders are included.
5. **Prototype interactive dashboards in Streamlit** using the scalable starter in `../streamlit-dashboard/`, then move stakeholder-facing reporting to Power BI/Tableau/Looker when governance and scheduled refresh are needed.

## Run the notebooks

From the repo root:

```powershell
uv sync
docker compose --env-file .env -f oracle-food-analysis/docker-compose.yml up -d
```

Open notebooks in `oracle-food-analysis/python-notebooks/` and select the `learning-sql` uv environment/kernel. Ensure `.env` contains Oracle credentials and the `VW_TOP_10_*` views exist (run `oracle-food-analysis/notebooks/reporting_views.ipynb`).
