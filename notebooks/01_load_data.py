# ============================================
# ShopSense Product Analytics
# Script: Load raw CSV data into MySQL
# Author: Brijesh Vaghela
# ============================================

import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import os
import time

# ============================================
# CONFIGURATION
# Set DB_PASSWORD as an environment variable:
#   Windows: $env:DB_PASSWORD = "your_password"
#   Linux/Mac: export DB_PASSWORD="your_password"
# ============================================

DB_CONFIG = {
    'host'    : os.getenv('DB_HOST', '127.0.0.1'),
    'user'    : os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'shopsense')
}

if not DB_CONFIG['password']:
    raise ValueError("DB_PASSWORD environment variable is not set.")

# ============================================
# LIST OF CSV FILES TO LOAD
# ============================================

RAW_DATA_PATH = 'data/raw'

FILES = [
    '2019-Oct.csv',
    '2019-Nov.csv',
    '2019-Dec.csv',
    '2020-Jan.csv',
    '2020-Feb.csv'
]

# ============================================
# CREATE SQLALCHEMY ENGINE
# This is what connects Python to MySQL
# ============================================

engine = create_engine(
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}?charset=utf8mb4"
)

# ============================================
# FUNCTION TO CLEAN AND LOAD ONE FILE
# ============================================

def count_source_rows(filepath):
    """Count data rows in the source CSV (excludes header).
    Used to validate the load didn't silently drop rows."""
    with open(filepath, 'rb') as f:
        return sum(1 for _ in f) - 1


def load_file(filename):

    filepath = os.path.join(RAW_DATA_PATH, filename)
    print(f"\n{'='*50}")
    print(f"Loading: {filename}")
    print(f"{'='*50}")

    expected_rows = count_source_rows(filepath)

    # Read CSV in chunks of 100,000 rows
    # This prevents RAM overload on large files
    chunk_size = 100000
    chunk_number = 0
    total_rows = 0

    for chunk in pd.read_csv(filepath, chunksize=chunk_size):

        chunk_number += 1

        # ----------------------------------------
        # CLEAN event_time column
        # Remove " UTC" from timestamp string
        # Convert to proper datetime format
        # ----------------------------------------
        chunk['event_time'] = chunk['event_time'].str.replace(' UTC', '', regex=False)
        chunk['event_time'] = pd.to_datetime(chunk['event_time'], errors='coerce')

        # ----------------------------------------
        # CLEAN price column
        # Fill missing prices with 0
        # ----------------------------------------
        chunk['price'] = pd.to_numeric(chunk['price'], errors='coerce').fillna(0)

        # ----------------------------------------
        # CLEAN text columns
        # Fill missing brand and category with NULL
        # ----------------------------------------
        chunk['brand']         = chunk['brand'].where(chunk['brand'].notna(), None)
        chunk['category_code'] = chunk['category_code'].where(chunk['category_code'].notna(), None)

        # ----------------------------------------
        # LOAD this chunk into MySQL
        # if_exists='append' adds to existing rows
        # ----------------------------------------
        chunk.to_sql(
            name      = 'raw_events',
            con       = engine,
            if_exists = 'append',
            index     = False
        )

        total_rows += len(chunk)
        print(f"  Chunk {chunk_number} loaded — {total_rows:,} rows so far")

    # ----------------------------------------
    # VALIDATE: loaded row count must match the
    # source file's data row count. A mismatch here
    # means rows were silently dropped mid-load
    # (e.g. a malformed row breaking a chunk boundary).
    # ----------------------------------------
    assert total_rows == expected_rows, (
        f"Row count mismatch in {filename}: "
        f"loaded {total_rows:,}, source has {expected_rows:,}. "
        f"Stopping — investigate before trusting downstream analysis."
    )

    print(f"\n✅ {filename} complete — {total_rows:,} total rows loaded "
          f"(validated against {expected_rows:,} source rows)")
    return total_rows


# ============================================
# MAIN EXECUTION
# Loop through all 5 files
# ============================================

if __name__ == '__main__':

    start_time = time.time()
    grand_total = 0

    for file in FILES:
        rows = load_file(file)
        grand_total += rows

    end_time = time.time()
    duration = round((end_time - start_time) / 60, 2)

    print(f"\n{'='*50}")
    print(f"🎉 ALL FILES LOADED SUCCESSFULLY")
    print(f"Total rows inserted : {grand_total:,}")
    print(f"Time taken          : {duration} minutes")
    print(f"{'='*50}")

    # Sanity check against the documented dataset scale (~20.7M rows).
    # A soft warning, not a hard failure — the exact count can vary by
    # a few rows depending on the Kaggle download, but a large gap
    # means something is wrong with the source files or the load.
    EXPECTED_APPROX = 20_692_840
    pct_diff = abs(grand_total - EXPECTED_APPROX) / EXPECTED_APPROX * 100
    if pct_diff > 1:
        print(f"⚠️  WARNING: loaded {grand_total:,} rows, expected "
              f"~{EXPECTED_APPROX:,} (±1%). Off by {pct_diff:.1f}% — "
              f"verify the source CSVs before trusting downstream analysis.")
    else:
        print(f"✅ Row count within expected range of ~{EXPECTED_APPROX:,}")