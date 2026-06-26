import streamlit as st
import pandas as pd

# ----------------------------------
# PAGE SETTINGS
# ----------------------------------
st.set_page_config(
    page_title="Mount Roofing RM Allocation",
    layout="wide"
)

# ----------------------------------
# TITLE
# ----------------------------------
st.title("🏭 Mount Roofing RM Allocation System")

st.markdown("---")

# ----------------------------------
# FILE UPLOADS
# ----------------------------------
planning_file = st.file_uploader(
    "Upload Planning File",
    type=["xlsx"]
)

rm_file = st.file_uploader(
    "Upload RM Stock File",
    type=["xlsx"]
)

db_file = st.file_uploader(
    "Upload DB File",
    type=["xlsx"]
)

# ----------------------------------
# STATUS
# ----------------------------------
if planning_file:
    st.success("Planning File Uploaded")

if rm_file:
    st.success("RM Stock File Uploaded")

if db_file:
    st.success("DB File Uploaded")

if planning_file and rm_file and db_file:

    st.success("All Files Uploaded Successfully")

    if st.button("Process Files"):

        try:

            st.info("Reading Files...")

            # --------------------------
            # READ EXCEL FILES
            # --------------------------
            planning_df = pd.read_excel(planning_file)

            rm_df = pd.read_excel(rm_file)

            db_df = pd.read_excel(db_file)

            st.success("Files Read Successfully")

            # --------------------------
            # FILE INFORMATION
            # --------------------------
            st.subheader("Planning File Information")

            st.write("Rows :", planning_df.shape[0])
            st.write("Columns :", planning_df.shape[1])

            st.write("Column Names")

            st.write(list(planning_df.columns))

            st.dataframe(planning_df.head())

            st.markdown("---")

            st.subheader("RM Stock File Information")

            st.write("Rows :", rm_df.shape[0])
            st.write("Columns :", rm_df.shape[1])

            st.write("Column Names")

            st.write(list(rm_df.columns))

            st.dataframe(rm_df.head())

            st.markdown("---")

            st.subheader("DB File Information")

            st.write("Rows :", db_df.shape[0])
            st.write("Columns :", db_df.shape[1])

            st.write("Column Names")

            st.write(list(db_df.columns))

            st.dataframe(db_df.head())

            st.success("Testing Completed Successfully")

        except Exception as e:

            st.error("Error While Reading Files")

            st.error(str(e))