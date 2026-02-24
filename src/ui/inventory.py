"""
UI component for inventory management.
Simplified for Turso-only data source.
"""
import streamlit as st
import pandas as pd
import time
from src.database.operations import upsert_symbol_mapping, delete_symbol_mapping

def render_inventory_ui(db_map, inventory_list):
    """Renders the inventory manager UI section."""
    st.subheader("📦 Inventory Manager")
    
    # --- SECTION 1: ADD NEW SYMBOL ---
    with st.container(border=True):
        st.write("### ➕ Add New Symbol")
        
        display_name = st.text_input("Display Name (Unique ID)", placeholder="e.g. BTCUSDT, AAPL, Gold").upper().strip()
        
        if st.button("Save New Symbol", type="primary", disabled=not display_name):
            if upsert_symbol_mapping(display_name):
                st.success(f"Saved {display_name}")
                time.sleep(0.5)
                st.rerun()

    # --- SECTION 2: TABLE VIEW ---
    st.write("### 📋 Current Inventory")
    if db_map:
        table_data = []
        for k in db_map.keys():
            table_data.append({
                "Display Name": k
            })
            
        st.dataframe(pd.DataFrame(table_data), use_container_width=True)
        
        st.write("#### 🗑️ Delete Symbol")
        c_del1, c_del2 = st.columns([3, 1])
        with c_del1:
            d_t = st.selectbox("Select Symbol to Delete", [""] + inventory_list, key="del_select")
        with c_del2:
            st.write("")
            st.write("")
            if st.button("Confirm Delete", type="primary", disabled=(not d_t)):
                delete_symbol_mapping(d_t)
                st.success(f"Deleted {d_t}")
                time.sleep(0.5)
                st.rerun()
