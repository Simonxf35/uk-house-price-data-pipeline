import duckdb
from pathlib import Path

DB_PATH = "housing.duckdb"
RAW_GLOB = "data/raw/pp_*.csv"

COLUMNS = ["transaction_id", "price", "date", "postcode", "property_type",
           "new_build", "tenure", "paon", "saon", "street", "locality",
           "town", "district", "county", "ppd_category", "status"]

def load_raw(con):
    con.sql(f"""
        CREATE OR REPLACE TABLE price_paid AS
        SELECT * FROM read_csv_auto('{RAW_GLOB}', names={COLUMNS})
    """)
    count = con.sql("SELECT count(*) FROM price_paid").fetchone()[0]
    print(f"Loaded {count:,} raw rows")

def clean(con):
    con.sql("""
        CREATE OR REPLACE TABLE price_paid_clean AS
        SELECT DISTINCT ON (transaction_id)
            transaction_id,
            price,
            CAST(date AS DATE) AS sale_date,
            EXTRACT(YEAR FROM CAST(date AS DATE)) AS sale_year,
            UPPER(postcode) AS postcode,
            property_type,
            new_build = 'Y' AS is_new_build,
            tenure,
            district,
            county
        FROM price_paid
        WHERE price > 0
        ORDER BY transaction_id, date DESC
    """)
    count = con.sql("SELECT count(*) FROM price_paid_clean").fetchone()[0]
    print(f"Cleaned table has {count:,} rows")

def main():
    con = duckdb.connect(DB_PATH)
    load_raw(con)
    clean(con)
    print(con.sql("""
        SELECT sale_year, count(*) AS n_sales, round(avg(price)) AS avg_price
        FROM price_paid_clean
        GROUP BY sale_year ORDER BY sale_year
    """))
    con.close()

if __name__ == "__main__":
    main()