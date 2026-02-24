"""
Database operations.
STRATEGY: 
1. Save everything as UTC Strings (Unique, Clean).
2. When viewing Health Matrix, convert back to US/Eastern to count 'Trading Days' correctly.
"""
import streamlit as st
import pandas as pd
import time
from src.database.connection import get_db_connection
from src.config import UTC, US_EASTERN

# --- Basic CRUD for Symbol Mapping ---

def get_symbol_map_from_db():
    """Fetches the complete symbol inventory from the table."""
    client = get_db_connection()
    if not client:
        return {}
    try:
        res = client.execute("""
            SELECT display_name 
            FROM market_symbols 
            ORDER BY display_name
        """).fetchall()
        
        inventory = {}
        for row in res:
            inventory[row[0]] = {}
        return inventory
    except Exception:
        return {}

def upsert_symbol_mapping(display_name):
    """Adds a symbol to the inventory."""
    client = get_db_connection()
    if not client:
        return False
    try:
        client.execute(
            "INSERT OR IGNORE INTO market_symbols (display_name) VALUES (?)",
            (display_name,)
        )
        client.commit()
        return True
    except Exception as e:
        st.error(f"Error saving symbol: {e}")
        return False

def delete_symbol_mapping(ticker):
    """Deletes a symbol."""
    client = get_db_connection()
    if not client:
        return False
    try:
        client.execute("DELETE FROM market_symbols WHERE display_name = ?", (ticker,))
        client.commit()
        return True
    except Exception as e:
        st.error(f"Error deleting symbol: {e}")
        return False

# --- MARKET DATA OPERATIONS ---

def save_data_to_turso(df: pd.DataFrame, logger=None):
    """
    Saves market data using INSERT OR REPLACE.
    CRITICAL: Normalizes timestamps to UTC strings to ensure uniqueness.
    """
    if df.empty:
        return False

    client = get_db_connection()
    if not client:
        return False

    try:
        # 1. Copy and Normalize Timestamp
        batch_df = df.copy()
        
        if not pd.api.types.is_datetime64_any_dtype(batch_df['timestamp']):
            batch_df['timestamp'] = pd.to_datetime(batch_df['timestamp'], utc=True)

        # 2. FORCE UTC CONVERSION
        if batch_df['timestamp'].dt.tz is not None:
            batch_df['timestamp'] = batch_df['timestamp'].dt.tz_convert(UTC)
        else:
            batch_df['timestamp'] = batch_df['timestamp'].dt.tz_localize(UTC)

        # 3. Create String for SQLite
        batch_df['timestamp_str'] = batch_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # 4. Prepare Batch
        rows_to_insert = []
        for _, row in batch_df.iterrows():
            rows_to_insert.append((
                row['timestamp_str'],
                row['symbol'],
                row['open'], row['high'], row['low'], row['close'], row['volume'],
                row['session']
            ))

        # 5. Execute Batch
        BATCH_SIZE = 100
        
        if logger:
            logger.log(f"   💾 Committing {len(rows_to_insert)} records...")

        for i in range(0, len(rows_to_insert), BATCH_SIZE):
            batch = rows_to_insert[i : i + BATCH_SIZE]
            placeholders = ", ".join(["(?, ?, ?, ?, ?, ?, ?, ?)"] * len(batch))
            flat_values = tuple(item for sublist in batch for item in sublist)
            
            query = f"""
                INSERT OR REPLACE INTO market_data 
                (timestamp, symbol, open, high, low, close, volume, session) 
                VALUES {placeholders}
            """
            client.execute(query, flat_values)
            time.sleep(0.05)
            
        client.commit()
        return True

    except Exception as e:
        err = f"Save Error: {e}"
        if logger: logger.log(f"   ❌ {err}")
        elif st.runtime.exists(): st.error(err)
        print(err)
        return False


def fetch_data_health_matrix(tickers: list, start_date, end_date, session_filter="Total"):
    """
    Fetches data, CONVERTS TO US/EASTERN, and then groups by day.
    """
    client = get_db_connection()
    if not client:
        return pd.DataFrame()

    start_str = f"{start_date} 00:00:00" 
    end_dt_buffer = end_date + pd.Timedelta(days=1)
    end_str = f"{end_dt_buffer} 23:59:59"

    placeholders = ",".join("?" * len(tickers))
    query = f"""
        SELECT timestamp, symbol, session
        FROM market_data 
        WHERE symbol IN ({placeholders}) 
          AND timestamp >= ? 
          AND timestamp <= ?
    """
    params = tuple(tickers + [start_str, end_str])
    
    try:
        res = client.execute(query, params).fetchall()
        if not res:
            return pd.DataFrame()
            
        df = pd.DataFrame([list(row) for row in res], columns=['timestamp', 'symbol', 'session'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(UTC)
        df['timestamp_et'] = df['timestamp'].dt.tz_convert(US_EASTERN)
        df['day'] = df['timestamp_et'].dt.date
        
        if session_filter != "Total":
            df = df[df['session'] == session_filter]
            
        df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]
        
        if df.empty:
            return pd.DataFrame()

        grouped = df.groupby(['symbol', 'day']).size().reset_index(name='candle_count')
        pivot_df = grouped.pivot(index='symbol', columns='day', values='candle_count')
        
        return pivot_df

    except Exception as e:
        st.error(f"Error fetching health matrix: {e}")
        return pd.DataFrame()
