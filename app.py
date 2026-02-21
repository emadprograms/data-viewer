import streamlit as st
from src.database.schema import init_db

# Page Config
# This serves as the "Home" page in the Multipage App structure.
st.set_page_config(
    page_title="Market Data Harvester", 
    layout="wide", 
    page_icon="🦁", 
    initial_sidebar_state="expanded"
)

def main():
    # Initialize DB (Ensure tables exist)
    init_db()
    
    st.title("🦁 Market Data Archive")
    st.markdown("""
    ### 📡 Automated Data Harvesting System
    The primary job of this repository is to automatically harvest **1-minute OHLCV candles** every day at **6 AM Bahrain time** via GitHub Workflows.
    
    The data is stored in the **Stock Data Archive** (Turso/libSQL) database.
    
    ---
    
    ### 🏥 Streamlit Role: Health Inspection
    In this new architecture, Streamlit serves as a **monitoring and diagnostic tool**:
    
    *   **Data Health Dashboard:** Check the completeness of the harvested data.
    *   **Database Inspector:** Peek into the raw records stored in Turso.
    *   **Inventory Manager:** Manage the list of symbols being harvested by the workflow.
    *   **Manual Harvester:** Use only for "gap filling" or manual fixes if the automated workflow misses a day.
    
    ---
    
    ### 🚀 Current Configuration
    *   **Primary Source:** Massive (Polygon.io) for full-day aggregates.
    *   **Schedule:** 6 AM Bahrain (3 AM UTC) daily, captures the full session data from the day that just concluded.
    *   **Database:** Turso 'Stock Data Archive'.
    """)
    
    st.divider()
    st.info("👈 **Select a health dashboard or inspector from the sidebar.**")

if __name__ == "__main__":
    main()