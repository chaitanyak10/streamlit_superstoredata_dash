import streamlit as st
import pandas as pd
import numpy as np


# Set app-wide layout
st.set_page_config(
    page_title="Superstoredata Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .title {
        background-color: #2E9AFE; /* BMW blue color */
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 2em;
        border-radius: 5px;
    }
    </style>
    <div class="title">Superstoredata Dashboard</div>
    """,
    unsafe_allow_html=True
)

# Load data
dataframe = pd.read_excel("Sample - Superstore.xls")

# Add filters at the top
st.header("Filters")

# Create columns for filters
filter_col1, filter_col2, filter_col3 = st.columns(3)

# Region filter
regions = dataframe['Region'].unique()
with filter_col1:
    selected_region = st.selectbox("Select Region", options=['All'] + list(regions))

# Segment filter
segments = dataframe['Segment'].unique()
with filter_col2:
    selected_segment = st.selectbox("Select Segment", options=['All'] + list(segments))

# Year filter
dataframe['Order Year'] = pd.to_datetime(dataframe['Order Date']).dt.year
years = sorted(dataframe['Order Year'].unique())
with filter_col3:
    selected_year = st.selectbox("Select Year", options=['All'] + list(years))

# Apply filters
filtered_df = dataframe.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_segment != 'All':
    filtered_df = filtered_df[filtered_df['Segment'] == selected_segment]
if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['Order Year'] == selected_year]

dataframe = filtered_df

# Calculate KPIs
total_sales = dataframe['Sales'].sum()
total_profit = dataframe['Profit'].sum()
profit_ratio = (total_profit / total_sales) * 100 if total_sales != 0 else 0
distinct_customers = dataframe['Customer ID'].nunique()

# Display KPIs

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales (in K)", f"${total_sales/1000:,.1f}K")
col2.metric("Total Profit (in K)", f"${total_profit/1000:,.1f}K")
col3.metric("Profit Ratio", f"{profit_ratio:.1f}%")
col4.metric("Distinct Customers", f"{distinct_customers}")

# Create a bar chart showing Sales by Sub-category with X axis as Sub-Category
sales_by_subcategory = dataframe.groupby('Sub-Category', as_index=False)['Sales'].sum()
sales_by_subcategory = sales_by_subcategory.sort_values(by='Sales', ascending=False)
st.bar_chart(sales_by_subcategory.set_index('Sub-Category')['Sales'])