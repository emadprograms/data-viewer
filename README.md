# 📈 Data Viewer

A Streamlit-based dashboard for visualizing and monitoring market data.

## 🛠 Features

- **Health Dashboard**: Monitor the status of daily harvests.
- **Data Inspection**: View detailed market data records from the Turso "Stock Data Archive".
- **Visual Analytics**: Interactive charts using `lightweight-charts`.

## 📁 Repository Structure

- `app.py`: Main Streamlit entry point.
- `pages/`: Additional dashboard sub-pages.
- `src/`:
  - `database/`: Turso connection and data retrieval logic.
  - `ui/`: Custom UI components and styling.

## 🚀 Usage

```bash
pip install -r requirements.txt
streamlit run app.py
```

---
*Created with ❤️ by Antigravity*
