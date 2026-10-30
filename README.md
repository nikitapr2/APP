# 🏥 Smart Hospital Queue Management System

**AI-Powered Smart Hospital Queue Management and Patient Waiting Time Reduction System**  
*Less Waiting. Better Care.*

---

## ⚡ Quick Start

### Step 1 — Install Python
Download Python 3.9+ from https://python.org if you haven't already.

### Step 2 — Install dependencies
Open a terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
streamlit run app.py
```

The browser will open automatically at **http://localhost:8501**

---

## 📋 Features

| Page | What it does |
|------|-------------|
| **Dashboard** | KPI cards, daily patient charts, doctor load, status donut |
| **Register Patient** | Form with auto token generation & wait-time estimate |
| **Patient Queue** | Doctor-wise live queue with status pills |
| **Analytics** | Trend charts, symptom frequency, age histogram, heatmap |
| **Patient Records** | Searchable table with CSV download |

---

## 🛠 Tech Stack
- **Python 3.9+**
- **Streamlit** — web framework
- **Plotly** — interactive charts
- **Pandas / NumPy** — data handling

---

## 📝 Notes
- All patient data is **sample/dummy data** for demonstration.
- Registered patients persist for the session only (no database).
- For a production system, connect a PostgreSQL or Firebase backend.
