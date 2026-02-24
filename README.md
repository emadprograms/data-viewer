# 📈 Data Viewer

A Streamlit-based dashboard for visualizing and monitoring market data stored in Turso.

## 🛠 Features

- **Health Dashboard**: Monitor the status and completeness of collected data.
- **Database Inspector**: View raw market records with high-performance interactive charts.
- **Visual Analytics**: Visual audit of data integrity using `lightweight-charts`.

## 📁 Repository Structure

- `streamlit_app.py`: Main Streamlit entry point.
- `pages/`: Individual dashboard sub-pages for Health and Inspection.
- `src/`:
  - `database/`: Turso connection and data operations.
  - `ui/`: Custom UI components for each dashboard.
  - `infisical_manager.py`: Secrets management via Infisical.

## 🚀 Usage

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---
*Created with ❤️ by Antigravity*
