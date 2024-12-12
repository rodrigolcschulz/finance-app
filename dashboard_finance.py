import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the financial data file
file_path = "gcdf_v3_finance.csv"
finance_data = pd.read_csv(file_path)

# Filter relevant data
financial_data = finance_data[
    ['Amount.(Constant.USD.2021)', 'Sector.Name', 'Recipient', 'Commitment.Year', 'Completion.Year']
].dropna()

# Convert columns to appropriate data types
financial_data['Amount.(Constant.USD.2021)'] = financial_data['Amount.(Constant.USD.2021)'].astype(float)
financial_data['Commitment.Year'] = financial_data['Commitment.Year'].astype(int)

# Streamlit App
st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("Financial Data Dashboard")
st.markdown("## Overview of Financial Data")

# Sidebar Filters
st.sidebar.header("Filters")
years = financial_data['Commitment.Year'].unique()
selected_years = st.sidebar.multiselect("Select Commitment Years:", options=sorted(years), default=sorted(years))

countries = financial_data['Recipient'].unique()
selected_countries = st.sidebar.multiselect("Select Countries:", options=sorted(countries), default=sorted(countries))

# Filter data based on selections
filtered_data = financial_data[
    (financial_data['Commitment.Year'].isin(selected_years)) &
    (financial_data['Recipient'].isin(selected_countries))
]

# Group by Sector for financial distribution
sector_finance = filtered_data.groupby('Sector.Name')['Amount.(Constant.USD.2021)'].sum().sort_values(ascending=False)

# Top 10 countries by financial amount
country_finance = filtered_data.groupby('Recipient')['Amount.(Constant.USD.2021)'].sum().reset_index()
country_finance.rename(columns={'Recipient': 'name', 'Amount.(Constant.USD.2021)': 'Total_Finance'}, inplace=True)
top_countries = country_finance.sort_values(by='Total_Finance', ascending=False).head(10)

# Annual commitments
annual_commitments = filtered_data.groupby('Commitment.Year')['Amount.(Constant.USD.2021)'].sum()

# Prepare data for the heatmap
heatmap_data = filtered_data.groupby(['Recipient', 'Commitment.Year'])['Amount.(Constant.USD.2021)'].sum().unstack(fill_value=0)

# Apply dark mode for plots
plt.style.use('dark_background')

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Financial Amount by Sector")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sector_finance.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Total Financial Amount by Sector')
    ax1.set_xlabel('Sector Name')
    ax1.set_ylabel('Total Amount (USD)')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)

    st.subheader("Annual Commitments Over Years")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    annual_commitments.plot(kind='line', marker='o', ax=ax2, color='orange')
    ax2.set_title('Annual Commitments Over Years')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Total Amount (USD)')
    st.pyplot(fig2)

with col2:
    st.subheader("Top 10 Countries by Financial Amount")
    fig3 = px.bar(top_countries, x='Total_Finance', y='name', orientation='h', color='Total_Finance',
                  title='Top 10 Countries by Financial Amount', labels={'name': 'Country'}, template='plotly_dark')
    st.plotly_chart(fig3)

    st.subheader("Financial Commitments by Country and Year")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap='viridis', annot=False, cbar_kws={'label': 'Total Financial Amount (USD)'}, ax=ax4)
    ax4.set_title('Financial Commitments by Country and Year')
    ax4.set_xlabel('Commitment Year')
    ax4.set_ylabel('Country')
    st.pyplot(fig4)

st.sidebar.markdown("---")
st.sidebar.write("Data Source: Financial Dataset")
