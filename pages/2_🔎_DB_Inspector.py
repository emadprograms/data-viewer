import streamlit as st
from src.database.operations import get_symbol_map_from_db
from src.ui.inspector import render_inspector_ui

st.set_page_config(
    page_title="DB Inspector | Data Viewer", 
    page_icon="🔎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔎 Database Inspector")

db_map = get_symbol_map_from_db()
symbol_list = sorted(list(db_map.keys()))

render_inspector_ui(symbol_list)
