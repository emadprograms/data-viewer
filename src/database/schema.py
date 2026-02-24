"""
Database schema initialization and table creation.
Includes strict PRIMARY KEY constraints to prevent duplication.
"""
import streamlit as st
from src.database.connection import get_db_connection


def init_db():
    """Initializes the database, creating tables if they don't exist."""
    client = get_db_connection()
    if not client:
        return
    
    try:
        # --- NEW SCALABLE SCHEMA ---
        # Only keeping display_name for symbols available in Turso
        client.execute("""
            CREATE TABLE IF NOT EXISTS market_symbols (
                display_name TEXT PRIMARY KEY
            )
        """)

        # Fresh Seed if empty
        row = client.execute("SELECT count(*) FROM market_symbols").fetchone()
        count = row[0] if row else 0
        
        if count == 0:
            # Fresh Seed
            tickers = [
                "SPY", "QQQ", "IWM", "DIA", "AMD", "AMZN", "AAPL", "NVDA", "TSLA",
                "BTCUSDT", "ETHUSDT", "CL=F", "GC=F", "VIX"
            ]
            for t in tickers:
                client.execute(
                    "INSERT OR IGNORE INTO market_symbols (display_name) VALUES (?)",
                    (t,)
                )
            client.commit()

        
        # Table for storing all market data
        # CRITICAL: PRIMARY KEY (symbol, timestamp) forces SQLite to reject duplicates.
        # We store timestamp as a UTC String to ensure strict uniqueness.
        client.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                open REAL, 
                high REAL, 
                low REAL, 
                close REAL, 
                volume REAL, 
                session TEXT,
                PRIMARY KEY (symbol, timestamp)
            )
        """)
        client.commit()
                
    except Exception as e:
        if st.runtime.exists():
            st.error(f"DB Init Error: {e}")
        else:
            print(f"DB Init Error: {e}")
