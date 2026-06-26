# FIFO Raw Material Coil Allocation System

Automates FIFO-based coil allocation for roofing panel production.

## Features
- Matches orders to top/bottom coils by brand preference
- Falls back to best available stock when exact match unavailable
- Calculates required KG using consumption-per-SQM master DB
- Outputs allocation, shortage report, and stock balance to Excel

## How to Run
pip install pandas openpyxl streamlit
streamlit run streamlit_app.py

## Inputs Required
- Planning File (production orders)
- RM Stock File (available coils with FIFO dates)
- DB File (consumption rates + brand master)
