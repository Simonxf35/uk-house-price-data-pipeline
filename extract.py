import requests
import os
from pathlib import Path
BASE_URL = "http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-{year}.csv"
BASE_URL = "2016, 2026" # Shows data from 2016-2025 period
RAW_DIR = Path("data/raw")


# Retrieves dataset from the hyperlink

def download_year(year: int) -> None:
    out_path = RAW_DIR / f"pp_{year}.csv"
    if out_path.exists():
        print(f"{year}: already downloaded, skipping process")
        return
    
    url = BASE_URL.format(year=year)
    response = requests.get(url, timeout=120)
    response.raise_for_status()

    out_path.write_bytes(response.content)
    size_mb = len(response.content) / 1e6
    print(f"{year}: downloaded ({size_mb: .1f} MB)")

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for year in year:
        download_year(year)

if __name__ == "__main__":
    main()
          