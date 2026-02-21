"""
Database connection management for Turso (libSQL).
"""
import streamlit as st
import libsql_experimental as libsql
import os


def get_db_connection():
    """Establishes a synchronous connection to the Turso database."""
    try:

        from src.infisical_manager import InfisicalManager
        mgr = InfisicalManager()
        
        url = mgr.get_secret("turso_arshademad_stockdataarchive_db_url")
        token = mgr.get_secret("turso_arshademad_stockdataarchive_auth_token")
        
        if not url or not token:
            if st.runtime.exists():
                st.error("Missing Turso credentials. Check Infisical Access.")
            return None
        
        # Connect using libsql-experimental (handles wss/https implicitly better)
        return libsql.connect(url, auth_token=token)
    except Exception as e:
        if st.runtime.exists():
            st.error(f"Failed to create Turso client: {e}")
        else:
            print(f"DB Connection Error: {e}")
        return None
