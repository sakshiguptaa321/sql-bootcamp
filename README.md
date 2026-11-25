# SQL Bootcamp

A hands-on SQL practice repository using SQLite and Jupyter notebooks. The exercises focus on defining tables, inserting data, and querying a food-orders dataset. A separate set of student-related CSV files is included for additional practice.

## Repository layout

- `food-analysis/`
  - `notebooks/`: SQL lessons, including DDL, DML, filtering and sorting, aggregations, and joins.
  - `data/`: CSV files for customers, products, orders, and order items.
  - `food_analysis.db`: local SQLite database used by the notebooks. It is generated locally and is not tracked by Git.
- `oracle-food-analysis/`
  - `docker-compose.yml`: Docker Compose config for the local Oracle Free database.
  - `notebooks/`: Oracle SQL notebooks (DDL, DML, and function practice).
  - `test.ipynb`: quick Oracle connection test.
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
6. `query_04_subqueries_sets.ipynb` — use subqueries and set operations.
7. `query_05_case_functions_nulls.ipynb` — categorize values and handle missing data with SQLite functions.
8. `query_06_window_functions.ipynb` — rank rows and calculate running totals.
9. `query_07_ctes_temp_tables.ipynb` — use CTEs, check data quality, and work with temporary tables.
10. `query_08_indexes_query_plans.ipynb` — compare SQLite query plans using a temporary indexed copy.
11. `query_09_transactions.ipynb` — practice `COMMIT` and `ROLLBACK` without changing the source data.

The `queries.ipynb` and `sql-notebook.ipynb` notebooks provide an overview of the query lessons and recommended order. If you rerun `dml.ipynb`, run `ddl.ipynb` first so the tables are empty.

## Oracle setup (Docker)

The Oracle exercises use a local [gvenzl/oracle-free](https://hub.docker.com/r/gvenzl/oracle-free) container and the notebooks in `oracle-food-analysis/`.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- Python dependencies installed with `uv sync` (includes `oracledb`, `sqlalchemy`, `python-dotenv`)

### Environment variables

Create a `.env` file in the repository root (it is git-ignored). Do not commit real credentials.

```env
ORACLE_USER=FOOD_ANALYSIS
ORACLE_PASSWORD=<app-user-password>
ORACLE_SYSTEM_PASSWORD=<oracle-system-password>
```

### Start / stop the database

Use the Compose file at `oracle-food-analysis/docker-compose.yml`:

```powershell
# Start (create/start container)
docker compose --env-file .env -f oracle-food-analysis/docker-compose.yml up -d

# Check status
docker ps -a --filter "name=learning-sql-oracle" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Stop
docker compose --env-file .env -f oracle-food-analysis/docker-compose.yml stop

# Start again after stop
docker compose --env-file .env -f oracle-food-analysis/docker-compose.yml start

# Remove container (keeps named volume/data)
docker compose --env-file .env -f oracle-food-analysis/docker-compose.yml down
```

### Connection details

- **Host:** `localhost`
- **Port:** `1522`
- **Service name:** `FREEPDB1` (use service name, not SID)
- **User:** `FOOD_ANALYSIS`
- **Password:** value of `ORACLE_PASSWORD` from `.env`

SQLAlchemy / ipython-sql connection URL format:

```text
oracle+oracledb://FOOD_ANALYSIS:<password>@localhost:1522?service_name=FREEPDB1
```

### Oracle notebooks

Run the Oracle notebooks in this order:

1. `oracle-food-analysis/test.ipynb` — verify the connection.
2. `oracle-food-analysis/notebooks/ddl.ipynb` — create/reset Oracle tables. **This resets exercise tables.**
3. `oracle-food-analysis/notebooks/dml.ipynb` — insert practice data.
4. `oracle-food-analysis/notebooks/day2_sql_functions.ipynb` — SQL function practice (read-only queries).

If you rerun `ddl.ipynb`, rerun `dml.ipynb` before querying.

### Power BI

Use **Get Data > Oracle database** (not SQL Server). Set:

- **Server:** `localhost:1522/FREEPDB1`
- **Authentication:** Database
- **User name:** `FOOD_ANALYSIS`
- **Password:** `ORACLE_PASSWORD` from `.env`

Power BI Desktop may require a compatible 64-bit Oracle client/ODP.NET provider. If you see `ORA-12154` with an alias like `test_oracle`, replace the server with `localhost:1522/FREEPDB1` or define the alias in the Oracle client `tnsnames.ora`.
