import streamlit as st
import subprocess
import os

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Mount Roofing FIFO Coil Allocation System",
    page_icon="🏭",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("🏭 Mount Roofing")
st.subheader("FIFO Coil Allocation System")

st.markdown("---")

st.write("""
Upload the Planning File, DB File and RM Stock File.

Click Generate FIFO Plan to create the allocation report.
""")

# ==========================================
# FILE UPLOADS
# ==========================================

planning_file = st.file_uploader(
    "📋 Upload Planning File",
    type=["xlsx"]
)

db_file = st.file_uploader(
    "📚 Upload DB File",
    type=["xlsx"]
)

rm_file = st.file_uploader(
    "📦 Upload RM Stock File",
    type=["xlsx"]
)

# ==========================================
# STATUS
# ==========================================

if planning_file:
    st.success("✅ Planning File Uploaded")

if db_file:
    st.success("✅ DB File Uploaded")

if rm_file:
    st.success("✅ RM Stock File Uploaded")

# ==========================================
# GENERATE FIFO
# ==========================================

if st.button("🚀 Generate FIFO Plan"):

    try:

        # ==================================
        # VALIDATION
        # ==================================

        if not planning_file:
            st.error("Please upload Planning File")
            st.stop()

        if not db_file:
            st.error("Please upload DB File")
            st.stop()

        if not rm_file:
            st.error("Please upload RM File")
            st.stop()

        # ==================================
        # SAVE FILES
        # ==================================

        with open("PLANNING FILE.xlsx", "wb") as f:
            f.write(planning_file.getbuffer())

        with open("DB.xlsx", "wb") as f:
            f.write(db_file.getbuffer())

        with open("11052026 (1).xlsx", "wb") as f:
            f.write(rm_file.getbuffer())

        st.success("✅ Files Saved Successfully")

        # ==================================
        # RM STOCK PROCESSOR
        # ==================================

        st.info("Creating RM Stock...")

        result1 = subprocess.run(
            ["python", "rm_stock_processor.py"],
            capture_output=True,
            text=True
        )

        st.text(result1.stdout)

        if result1.returncode != 0:

            st.error("RM Stock Processor Failed")

            st.code(result1.stderr)

            st.stop()

        # ==================================
        # FIFO ALLOCATION
        # ==================================

        st.info("Running FIFO Allocation...")

        result2 = subprocess.run(
            ["python", "final_allocator_v2.py"],
            capture_output=True,
            text=True
        )

        st.text(result2.stdout)

        if result2.returncode != 0:

            st.error("FIFO Allocation Failed")

            st.code(result2.stderr)

            st.stop()

        # ==================================
        # DOWNLOAD RESULT
        # ==================================

        if os.path.exists("FIFO_RESULT.xlsx"):

            st.success("✅ FIFO Result Ready")

            with open(
                "FIFO_RESULT.xlsx",
                "rb"
            ) as file:

                file_data = file.read()

            st.download_button(
                label="📥 Download FIFO Result",
                data=file_data,
                file_name="FIFO_RESULT.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:

            st.error(
                "FIFO_RESULT.xlsx was not created"
            )

    except Exception as e:

        st.error(
            f"Error : {str(e)}"
        )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Mount Roofing | FIFO Coil Allocation System"
)