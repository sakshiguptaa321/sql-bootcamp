# SQL Bootcamp

A hands-on SQL practice repository using SQLite and Jupyter notebooks. The exercises focus on defining tables, inserting data, and querying a food-orders dataset. A separate set of student-related CSV files is included for additional practice.

## Repository layout

- `food-analysis/`
  - `notebooks/`: SQL lessons, including DDL, DML, filtering and sorting, aggregations, and joins.
  - `data/`: CSV files for customers, products, orders, and order items.
  - `food_analysis.db`: local SQLite database used by the notebooks. It is generated locally and is not tracked by Git.
- `student-analysis/data/`: CSV files for students, marks, fees, faculty, departments, courses, and attendance.
- `pyproject.toml` and `uv.lock`: Python project configuration and locked dependencies.

## Setup

Requirements: Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).

From the repository root, install the project dependencies:

```shell
uv sync
```

Open the notebooks in `food-analysis/notebooks/` with VS Code and select the Python environment created by `uv sync` as the notebook kernel. The VS Code Jupyter extension may be needed to run notebooks.

## Food analysis exercises

Run the notebooks in this order:

1. `ddl.ipynb` — create the SQLite schema. **This resets the exercise tables.**
2. `dml.ipynb` — insert the practice data.
3. `query_01_filter_sort.ipynb` — select, filter, and sort records.
4. `query_02_aggregations.ipynb` — summarize data with aggregate functions, `GROUP BY`, and `HAVING`.
5. `query_03_joins.ipynb` — combine related tables with joins.

The `queries.ipynb` and `sql-notebook.ipynb` notebooks provide an overview of the query lessons and recommended order. If you rerun `dml.ipynb`, run `ddl.ipynb` first so the tables are empty.
