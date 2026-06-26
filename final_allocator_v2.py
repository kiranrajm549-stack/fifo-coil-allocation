 
# final_allocator_brand_fifo.py
# ONE ORDER = ONE BRAND
# SELECT BRAND WITH MAX AVAILABLE STOCK
# FIFO INSIDE SELECTED BRAND

import pandas as pd

print("STARTED")

planning = pd.read_excel("PLANNING FILE.xlsx")

cons_db = pd.read_excel(
    "DB.xlsx",
    sheet_name="DB_CLEAN"
)

top_brand_db = pd.read_excel(
    "DB.xlsx",
    sheet_name="TOP_BRAND_MASTER"
)

bot_brand_db = pd.read_excel(
    "DB.xlsx",
    sheet_name="BOT_BRAND_MASTER"
)

rm = pd.read_excel("RM_STOCK_READY.xlsx")

rm["OPENING KG"] = rm["KG"]

# -----------------------------
# BUILD MAPS
# -----------------------------








consumption_log = []
shortage_log = []


def allocate_with_exact_and_fallback(
        wo_no,
        required_kg,
        planning_coil,
        allowed_brands,
        rm_stock,
        coil_type
):
    if pd.isna(required_kg) or required_kg <= 0:
        return "", [], 0, 0
    
    exact_stock = rm_stock[
        (rm_stock["TYPE"] == coil_type)
        &
        (
            rm_stock["FULL COIL NAME"]
            .astype(str)
            .str.strip()
            ==
            str(planning_coil).strip()
        )
    ]

    exact_qty = exact_stock["KG"].sum()

    if exact_qty > 0:

        selected_brand = planning_coil

    else:

        candidates = []

        for brand in allowed_brands:

            qty = rm_stock[
                (rm_stock["TYPE"] == coil_type)
                &
                (
                    rm_stock["FULL COIL NAME"]
                    .astype(str)
                    .str.strip()
                    ==
                    str(brand).strip()
                )
            ]["KG"].sum()

            candidates.append({

                "BRAND": brand,

                "AVAILABLE": qty

            })

        capable = [

            x for x in candidates

            if x["AVAILABLE"] >= required_kg

        ]

        if len(capable) > 0:

            capable = sorted(

                capable,

                key=lambda x:

                x["AVAILABLE"]
                -
                required_kg

            )

            selected_brand = capable[0]["BRAND"]

        else:

            if len(candidates) == 0:

                return "", [], 0, required_kg

            selected_brand = max(

                candidates,

                key=lambda x:

                x["AVAILABLE"]

            )["BRAND"]

    brand_stock = rm_stock[
        (rm_stock["TYPE"] == coil_type)
        &
        (
            rm_stock["FULL COIL NAME"]
            .astype(str)
            .str.strip()
            ==
            str(selected_brand).strip()
        )
    ].sort_values(
        "RECEIVED DATE"
    )

    balance = required_kg

    allocated = 0

    coils_used = []

    for idx, row in brand_stock.iterrows():

        if balance <= 0:
            break

        available = float(
            rm_stock.loc[idx, "KG"]
        )

        if available <= 0:
            continue

        use_qty = min(
            balance,
            available
        )

        rm_stock.loc[idx, "KG"] = (
            available - use_qty
        )

        allocated += use_qty

        balance -= use_qty

        coils_used.append(
            f"{row['COIL NO']} "
            f"({round(use_qty,2)} KG)"
        )
        consumption_log.append({

            "W.O NO":
            wo_no,

            "COIL NO":
            row["COIL NO"],

            "FULL COIL NAME":
            row["FULL COIL NAME"],

            "TYPE":
            coil_type,

            "USED KG":
            round(use_qty,2),

            "BALANCE AFTER":
            round(
                rm_stock.loc[idx, "KG"],
                2
            )

        })
    return (
        selected_brand,
        coils_used,
        round(allocated,2),
        round(balance,2)
    )


top_output = []
bot_output = []

for _, row in planning.iterrows():

    rmt = pd.to_numeric(row.get("TOTAL RMT"), errors="coerce")

    if pd.isna(rmt):
        continue

    # TOP
    top_colour = " ".join(
    str(row.get("TOP COIL","")).split()
    )
    

    match = cons_db[
    cons_db["TOP COIL"]
    .astype(str)
    .str.strip()
    ==
    top_colour
    ]

       

    if len(match):
            
            

            
            
            cons_series = pd.to_numeric(
                match["CONSUMPTION PER SQM"],
                errors="coerce"
            ).dropna()

            if len(cons_series) == 0:

                cons = None

            else:

                cons = cons_series.iloc[0]

            if pd.isna(cons):

                req = 0
                brand = ""
                coils = []
                alloc = 0
                short = 0

            else:

                req = round(rmt * cons, 2)
                print("RMT =", rmt)
                print("CONS =", cons)
                print("REQ =", req)

                brand_match = top_brand_db[
                    top_brand_db["TOP COLOUR"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    ==
                    str(top_colour).strip().upper()
                ]

                allowed_brands = []

                if len(brand_match):

                    for i in range(1,11):

                        col = f"COIL-{i}"

                        if (
                            col in brand_match.columns
                            and
                            pd.notna(
                                brand_match.iloc[0][col]
                            )
                        ):

                            allowed_brands.append(
                                str(
                                    brand_match.iloc[0][col]
                                ).strip()
                            )

                

                brand, coils, alloc, short = allocate_with_exact_and_fallback(
                    row.get("W.O NO",""),
                    req,
                    top_colour,
                    allowed_brands,
                    rm,
                    "TOP"
                )        
            

            top_output.append({

                "W.O NO":
                row.get("W.O NO",""),

                "CUSTOMER NAME":
                row.get("CUSTOMER NAME",""),

                "MARKETING NAME":
                row.get("MARKETING NAME",""),

                "REGION":
                row.get("REGION",""),

                "STATUS":
                row.get("STATUS",""),

                "PO NO":
                row.get("PO NO",""),

                "TYPE":
                row.get("TYPE",""),

                "TOTAL RMT":
                rmt,

                "TOP COIL":
                top_colour,

                "SELECTED BRAND":
                brand,

                "REQUIRED KG":
                req,

                "ALLOCATED KG":
                alloc,

                "SHORT KG":
                short,

                "COILS USED":
                " | ".join(coils)

             })

    # BOT
    bot_colour = " ".join(
    str(row.get("BOTTOM COIL","")).split()
    )

    if bot_colour and bot_colour != "nan":

        match = cons_db[
            cons_db["BOTTOM COIL"]
            .astype(str)
            .str.strip()
            ==
            bot_colour
        ]

        if len(match):

            cons = pd.to_numeric(
                match.iloc[0]["CONSUMPTION PER SQM.1"],
                errors="coerce"
            )

            if pd.isna(cons):

                req = 0
                brand = ""
                coils = []
                alloc = 0
                short = 0

            else:

                req = round(rmt * cons, 2)

                brand_match = bot_brand_db[
                    bot_brand_db["BOT COLOUR"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    ==
                    str(bot_colour).strip().upper()
                ]

                allowed_brands = []

                if len(brand_match):

                    for i in range(1,11):

                        col = f"COIL-{i}"

                        if (
                            col in brand_match.columns
                            and
                            pd.notna(
                                brand_match.iloc[0][col]
                            )
                        ):

                            allowed_brands.append(
                                str(
                                    brand_match.iloc[0][col]
                                ).strip()
                            )

                brand, coils, alloc, short = allocate_with_exact_and_fallback(
                    row.get("W.O NO",""),
                    req,
                    bot_colour,
                    allowed_brands,
                    rm,
                    "BOT"
                )

            bot_output.append({

                "W.O NO":
                row.get("W.O NO",""),

                "CUSTOMER NAME":
                row.get("CUSTOMER NAME",""),

                "MARKETING NAME":
                row.get("MARKETING NAME",""),

                "REGION":
                row.get("REGION",""),

                "STATUS":
                row.get("STATUS",""),

                "PO NO":
                row.get("PO NO",""),

                "TYPE":
                row.get("TYPE",""),

                "TOTAL RMT":
                rmt,

                "BOTTOM COIL":
                bot_colour,

                "SELECTED BRAND":
                brand,

                "REQUIRED KG":
                req,

                "ALLOCATED KG":
                alloc,

                "SHORT KG":
                short,

                "COILS USED":
                " | ".join(coils)

             })

top_df = pd.DataFrame(top_output)
bot_df = pd.DataFrame(bot_output)

balance_df = rm.copy()
balance_df["CONSUMED KG"] = balance_df["OPENING KG"] - balance_df["KG"]
balance_df.rename(columns={"KG":"BALANCE KG"}, inplace=True)

consumption_df = pd.DataFrame(consumption_log)

shortage_df = top_df[
    top_df["SHORT KG"] > 0
].copy()

if len(bot_df) > 0:

    shortage_df = pd.concat([
        shortage_df,
        bot_df[bot_df["SHORT KG"] > 0]
    ])

summary_df = pd.DataFrame({

    "METRIC":[

        "TOP ORDERS",
        "BOT ORDERS",
        "TOTAL ORDERS",

        "TOTAL TOP REQUIRED KG",
        "TOTAL BOT REQUIRED KG",

        "TOTAL TOP ALLOCATED KG",
        "TOTAL BOT ALLOCATED KG",

        "TOTAL SHORT KG",

        "TOTAL COILS CONSUMED"

    ],

    "VALUE":[

        len(top_df),

        len(bot_df),

        len(top_df)+len(bot_df),

        top_df["REQUIRED KG"].sum(),

        bot_df["REQUIRED KG"].sum(),

        top_df["ALLOCATED KG"].sum(),

        bot_df["ALLOCATED KG"].sum(),

        top_df["SHORT KG"].sum()
        +
        bot_df["SHORT KG"].sum(),

        len(consumption_df)

    ]

})

with pd.ExcelWriter(
        "FIFO_RESULT.xlsx",
        engine="openpyxl"
) as writer:

    top_df.to_excel(
        writer,
        sheet_name="TOP",
        index=False
    )

    bot_df.to_excel(
        writer,
        sheet_name="BOT",
        index=False
    )

    balance_df.to_excel(
        writer,
        sheet_name="STOCK BALANCE",
        index=False
    )

    consumption_df.to_excel(
        writer,
        sheet_name="COIL CONSUMPTION",
        index=False
    )

    shortage_df.to_excel(
        writer,
        sheet_name="SHORTAGE REPORT",
        index=False
    )

    summary_df.to_excel(
        writer,
        sheet_name="SUMMARY",
        index=False
    )

print("FIFO_RESULT.xlsx CREATED")
