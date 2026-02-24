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
        # --- PRIMARY INVENTORY TABLE ---
        # Reverted to symbol_map
        client.execute("""
            CREATE TABLE IF NOT EXISTS symbol_map (
                display_name TEXT PRIMARY KEY,
                yahoo_ticker TEXT,
                massive_ticker TEXT,
                binance_ticker TEXT
            )
        """)

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
            print(f"DB Error: {e}")
