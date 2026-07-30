import duckdb

DB_PATH = "housing.duckdb"

def build_dim_location(con):
    con.sql("""
        CREATE OR REPLACE TABLE dim_location AS
        SELECT
            ROW_NUMBER() OVER () AS location_id,
            postcode,
            district,
            county
        FROM (
            SELECT DISTINCT postcode, district, county
            FROM price_paid_clean
        )
    """)
    count = con.sql("SELECT count(*) FROM dim_location").fetchone()[0]
    print(f"dim_location: {count:,} rows")

def build_dim_date(con):
    con.sql("""
        CREATE OR REPLACE TABLE dim_date AS
        SELECT
            ROW_NUMBER() OVER () AS date_id,
            sale_date,
            sale_year,
            EXTRACT(MONTH FROM sale_date) AS sale_month,
            EXTRACT(QUARTER FROM sale_date) AS sale_quarter
        FROM (
            SELECT DISTINCT sale_date, sale_year
            FROM price_paid_clean
        )
    """)
    count = con.sql("SELECT count(*) FROM dim_date").fetchone()[0]
    print(f"dim_date: {count:,} rows")

def build_fact_sale(con):
    con.sql("""
        CREATE OR REPLACE TABLE fact_sale AS
        SELECT
            c.transaction_id,
            c.price,
            l.location_id,
            d.date_id,
            c.property_type,
            c.is_new_build,
            c.tenure
        FROM price_paid_clean c
        JOIN dim_location l
            ON c.postcode = l.postcode
            AND c.district = l.district
            AND c.county = l.county
        JOIN dim_date d
            ON c.sale_date = d.sale_date
    """)
    count = con.sql("SELECT count(*) FROM fact_sale").fetchone()[0]
    print(f"fact_sale: {count:,} rows")

def main():
    con = duckdb.connect(DB_PATH)
    build_dim_location(con)
    build_dim_date(con)
    build_fact_sale(con)

    print(con.sql("""
        SELECT d.sale_year, l.county, round(avg(f.price)) AS avg_price, count(*) AS n_sales
        FROM fact_sale f
        JOIN dim_date d ON f.date_id = d.date_id
        JOIN dim_location l ON f.location_id = l.location_id
        WHERE l.county = 'GREATER LONDON'
        GROUP BY d.sale_year, l.county
        ORDER BY d.sale_year
    """))
    con.close()

if __name__ == "__main__":
    main()
