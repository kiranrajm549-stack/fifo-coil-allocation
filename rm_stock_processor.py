import pandas as pd

print("STARTED")

# ==========================
# LOAD RM FILE
# ==========================

file_name = "11052026 (1).xlsx"

xls = pd.ExcelFile(file_name)

print("SHEETS FOUND:")
print(xls.sheet_names)

# ==========================
# COIL STOCK
# ==========================

coil_stock = pd.read_excel(
    file_name,
    sheet_name="COIL STOCK"
)

# ==========================
# BELOW 250 KG
# ==========================

below_250 = pd.read_excel(
    file_name,
    sheet_name="BELOW 250 KG"
)

# ==========================
# COMBINE
# ==========================

rm = pd.concat(
    [coil_stock, below_250],
    ignore_index=True
)

print("ROWS AFTER COMBINE:", len(rm))

# ==========================
# CLEAN COLUMN NAMES
# ==========================

rm.columns = rm.columns.str.strip()

print("COLUMNS:")
print(rm.columns.tolist())

# ==========================
# DATE
# ==========================

rm["RECEIVED DATE"] = pd.to_datetime(
    rm["RECEIVED DATE"],
    dayfirst=True,
    errors="coerce"
)

# ==========================
# KG
# ==========================

rm["KG"] = (
    pd.to_numeric(
        rm["WEIGHT IN TON"],
        errors="coerce"
    ) * 1000
)

# ==========================
# THICKNESS VALUE
# ==========================

rm["THICKNESS VALUE"] = (
    rm["THICKNES"]
    .astype(str)
    .str.extract(r"(\d+\.\d+)")
)

# ==========================
# WIDTH
# ==========================

rm["WIDTH"] = (
    rm["THICKNES"]
    .astype(str)
    .str.extract(r"X(\d+)")
)

rm["WIDTH"] = pd.to_numeric(
    rm["WIDTH"],
    errors="coerce"
)

# ==========================
# TYPE
# Excel Logic:
# IF(WIDTH>1200,"TOP","BOT")
# ==========================

rm["TYPE"] = rm["WIDTH"].apply(
    lambda x: "TOP" if x > 1200 else "BOT"
)

# ==========================
# FULL COIL NAME
# ==========================

rm["FULL COIL NAME"] = (
    rm["THICKNESS VALUE"].astype(str)
    + " "
    + rm["COLOUR"].astype(str)
    + " "
    + rm["MAKE"].astype(str)
)

# ==========================
# FIFO SORT
# ==========================

rm = rm.sort_values(
    "RECEIVED DATE",
    ascending=True
)

# ==========================
# SAVE
# ==========================

rm.to_excel(
    "RM_STOCK_READY.xlsx",
    index=False
)

print("================================")
print("RM_STOCK_READY.xlsx CREATED")
print("TOTAL RECORDS =", len(rm))
print("TOP COILS =", len(rm[rm["TYPE"] == "TOP"]))
print("BOT COILS =", len(rm[rm["TYPE"] == "BOT"]))
print("================================")