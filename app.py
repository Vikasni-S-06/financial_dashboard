import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("expenses.csv", parse_dates=['Date'])
    print("✅ Dataset loaded with shape:", df.shape)
    df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

st.title("💰 Financial Dashboard (Advanced)")

# Sidebar filters
st.sidebar.header("🔍 Filters")
users = st.sidebar.multiselect("User", df['User'].unique(), default=df['User'].unique())
types = st.sidebar.multiselect("Transaction Type", df['Type'].unique(), default=df['Type'].unique())
methods = st.sidebar.multiselect("Payment Method", df['PaymentMethod'].unique(), default=df['PaymentMethod'].unique())
locations = st.sidebar.multiselect("Location", df['Location'].unique(), default=df['Location'].unique())

# Apply filters
filtered_df = df[
    df['User'].isin(users) &
    df['Type'].isin(types) &
    df['PaymentMethod'].isin(methods) &
    df['Location'].isin(locations)
]

st.subheader("📅 Transactions Over Time")
time_chart = filtered_df.groupby(['YearMonth', 'Type'])['Amount'].sum().reset_index()
fig_time = px.bar(time_chart, x='YearMonth', y='Amount', color='Type', barmode='group')
st.plotly_chart(fig_time, use_container_width=True)

st.subheader("📊 Category Breakdown")
category_chart = filtered_df.groupby(['Category'])['Amount'].sum().reset_index()
fig_category = px.pie(category_chart, names='Category', values='Amount', title="Spending by Category")
st.plotly_chart(fig_category, use_container_width=True)

st.subheader("💳 Payment Method Usage")
payment_chart = filtered_df.groupby(['PaymentMethod'])['Amount'].sum().reset_index()
fig_payment = px.bar(payment_chart, x='PaymentMethod', y='Amount', color='PaymentMethod')
st.plotly_chart(fig_payment, use_container_width=True)

st.subheader("📍 Spending by Location")
location_chart = filtered_df.groupby(['Location'])['Amount'].sum().reset_index()
fig_location = px.bar(location_chart, x='Location', y='Amount', color='Location')
st.plotly_chart(fig_location, use_container_width=True)

st.subheader("🔁 Recurring vs Non-Recurring")
recurring_chart = filtered_df.groupby(['Recurring'])['Amount'].sum().reset_index()
fig_recurring = px.pie(recurring_chart, names='Recurring', values='Amount')
st.plotly_chart(fig_recurring, use_container_width=True)

st.subheader("📄 Raw Data")
st.dataframe(filtered_df)
