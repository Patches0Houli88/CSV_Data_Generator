import streamlit as st
import pandas as pd
import numpy as np
import random
from faker import Faker
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

fake = Faker()

st.set_page_config(page_title="CSV Data Generator", layout="wide")
st.title("🧪 Custom CSV Data Generator")

st.sidebar.header("🛠️ Schema Builder")

# --- Schema Creation --- #
column_names = []
column_types = []
data_types = [
    "name", "int", "float", "float_normal", "bool", "date", "city", "state", "zip", "category"
]

with st.sidebar.form("schema_form"):
    num_rows = st.number_input("Number of Rows", min_value=10, max_value=10000, value=100)
    num_cols = st.number_input("Number of Columns", min_value=1, max_value=20, value=5)

    for i in range(int(num_cols)):
        col1, col2 = st.columns([2, 2])
        with col1:
            name = st.text_input(f"Column {i+1} Name", key=f"name_{i}")
        with col2:
            dtype = st.selectbox(f"Column {i+1} Type", data_types, key=f"dtype_{i}")

        column_names.append(name)
        column_types.append(dtype)

    submitted = st.form_submit_button("Generate Data")

# --- Data Generator --- #
def generate_column(dtype):
    if dtype == "name":
        return fake.name()
    elif dtype == "int":
        return random.randint(1, 1000)
    elif dtype == "float":
        return round(random.uniform(10, 1000), 2)
    elif dtype == "float_normal":
        return round(np.random.normal(500, 150), 2)
    elif dtype == "bool":
        return random.choice([True, False])
    elif dtype == "date":
        return fake.date_between(start_date='-3y', end_date='today')
    elif dtype == "city":
        return fake.city()
    elif dtype == "state":
        return fake.state()
    elif dtype == "zip":
        return fake.zipcode()
    elif dtype == "category":
        return random.choice(['A', 'B', 'C'])
    return None

# --- Main Execution --- #
if submitted:
    data = []
    for _ in range(num_rows):
        row = [generate_column(dtype) for dtype in column_types]
        data.append(row)

    df = pd.DataFrame(data, columns=column_names)

    st.success("✅ Data generated successfully!")
    st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode(), "generated_data.csv", "text/csv")

    # --- Data Preview --- #
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # --- Auto Visual Summary --- #
    st.subheader("📈 Auto Visual Summary")
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            st.write(f"**{col}**")
            fig, ax = plt.subplots()
            df[col].hist(bins=20, ax=ax)
            st.pyplot(fig)
        elif df[col].dtype == 'object' or df[col].dtype == 'bool':
            st.write(f"**{col}**")
            st.bar_chart(df[col].value_counts())

    # --- Data Quality Report --- #
    st.subheader("🧪 Data Quality Report")
    st.write("**Null Values per Column:**")
    st.write(df.isnull().sum())
    st.write("**Duplicate Rows:**")
    st.write(df.duplicated().sum())
