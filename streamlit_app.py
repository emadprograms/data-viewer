import streamlit as st
from src.database.schema import init_db

# Page Config
st.set_page_config(
    page_title="Market Data Viewer", 
    layout="wide", 
    page_icon="📊", 
    initial_sidebar_state="expanded"
)

def main():
    # Initialize DB (Ensure tables exist)
    init_db()
    
    st.title("📊 Market Data Viewer")
    st.markdown("""
    This application serves as a **monitoring and diagnostic tool** for the market data stored in the Turso database.
    
    ---
    
    ### 🏥 Features
    
    *   **Data Health Dashboard:** Check the completeness and integrity of stored data.
    *   **Database Inspector:** Browse and visualize the raw records.
    
    ---
    
    ### 🚀 Configuration
    *   **Database:** Turso 'Stock Data Archive'.
    """)
    
    st.divider()
    st.info("👈 **Select a dashboard or inspector from the sidebar.**")

if __name__ == "__main__":
    main()
