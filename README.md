UK House Price Data Pipeline:

This is a data pipeline based around 10 years of UK residential Property transactions gathered from the HM Land Registry's Price Paid Data, this project aids to demonstrate a successful understanding of the ETL process through the using the techniques relating to data engineering, extraction, transformation, warehouse modelling and orchestration.

Overview

In an attempt to produce a real world scenario, the dataset used is from publicly available government data, assuring quality, authenticity and usability as this data is updated periodically every every in April. Working understand this framework assures that the creation of the ETL is within a professional standard as one would expect within a professional working environment. The purpose of the ETL is to produce a clean, queryable warehouse suitable for analysis and dashboarding.

Data source: HM Land Registry Price Paid Data
— over 24 million property sale records for England and Wales dating back to 1995,
released under the Open Government Licence.

Scope: 2016–2025 (10 full calendar years)

Architecture

Extract (HMLR CSV) → Raw store (data/raw) → Transform (DuckDB SQL)
    → Warehouse (star schema) → Serve (dashboard)

Extract — Downloads yearly Price Paid Data CSV files directly from HM Land
Registry's public S3 bucket. Idempotent: skips files already downloaded.
Raw store — Untouched source CSVs, kept separate from processed data so the
pipeline can always be re-run from the original source.
Transform — Uses DuckDB to clean, deduplicate, and type the data without loading
the full dataset into memory (chosen specifically to handle multi-GB data on
consumer hardware).
Warehouse — Cleaned data modelled into a star schema for analytical querying.
Serve — Data made available for dashboarding / visualisation.


Tech stack


Python — extraction and orchestration logic
DuckDB — out-of-core SQL transformation engine
SQL — data modelling (star schema)
Postgres (planned) — warehouse target for the modelled data
pytest (planned) — data quality tests


Project structure

uk-house-price-pipeline/
├── extract.py          # Downloads raw CSVs from HM Land Registry
├── transform.py         # DuckDB cleaning and modelling logic
├── load.py               # Loads cleaned data into the warehouse
├── config.py             # URLs, file paths, year range constants
├── requirements.txt
├── data/
│   ├── raw/               # Untouched source CSVs (gitignored)
│   └── processed/         # Cleaned output (gitignored)
└── tests/
    └── test_transform.py

Getting started

bashgit clone https://github.com/Simonxf35/uk-house-price-data-pipeline.git
cd uk-house-price-data-pipeline
pip install -r requirements.txt
python extract.py
python transform.py

Data notes


Raw CSV files have no header row; column names are applied manually in code to
match HM Land Registry's documented schema.
The two most recent months of any given period are typically incomplete, since
registration of a property sale can lag the actual transaction by weeks to months.
Category B transactions (repossessions, transfers, buy-to-lets) are only identifiable
from October 2013 onward.


Licence and attribution:

Contains HM Land Registry data © Crown copyright and database right 2026.
This data is licensed under the Open Government Licence v3.0.

Roadmap:

 Star schema warehouse implementation (Postgres)
 Data quality tests (row counts, null checks, duplicate detection)
 Orchestration (Airflow or Prefect scheduled runs)
 Dashboard / visualisation layer