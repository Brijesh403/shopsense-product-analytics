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
# Update password to your MySQL root password
# ============================================

DB_CONFIG = {
    'host'    : '127.0.0.1',
    'user'    : 'root',
    'password': '1998',
    'database': 'shopsense'
}

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

def load_file(filename):

    filepath = os.path.join(RAW_DATA_PATH, filename)
    print(f"\n{'='*50}")
    print(f"Loading: {filename}")
    print(f"{'='*50}")

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

    print(f"\n✅ {filename} complete — {total_rows:,} total rows loaded")
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