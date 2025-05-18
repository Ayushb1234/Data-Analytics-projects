
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIG ---
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

# --- TITLE ---
st.title("🛍️ Retail Sales & Customer Segmentation Dashboard")

# --- SIDEBAR FILE UPLOAD ---
st.sidebar.header("Upload Your Data")
retail_file = st.sidebar.file_uploader("Upload Cleaned Retail CSV", type=["csv"])
rfm_file = st.sidebar.file_uploader("Upload RFM Segmentation CSV", type=["csv"])
forecast_file = st.sidebar.file_uploader("Upload Sales Forecast CSV (Optional)", type=["csv"])

# --- LOAD DATA ---
if retail_file:
    df = pd.read_csv(retail_file, parse_dates=['InvoiceDate'])
    st.subheader("📦 Retail Data Preview")
    st.dataframe(df.head())

    # --- SALES TRENDS ---
    st.subheader("📈 Sales Over Time")
    df['Date'] = df['InvoiceDate'].dt.date
    daily_sales = df.groupby('Date')['TotalPrice'].sum().reset_index()
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=daily_sales, x='Date', y='TotalPrice', ax=ax1)
    ax1.set_title("Daily Revenue Trend")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Revenue")
    st.pyplot(fig1)

    # --- TOP PRODUCTS ---
    st.subheader("🏆 Top 10 Selling Products")
    top_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_products)

# --- RFM ANALYSIS ---
if rfm_file:
    rfm = pd.read_csv(rfm_file)
    st.subheader("🧠 Customer Segmentation (RFM)")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Customers", len(rfm))
        st.dataframe(rfm[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Segment']].head())

    with col2:
        segment_count = rfm['Segment'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(segment_count, labels=segment_count.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Customer Segment Distribution")
        st.pyplot(fig2)

# --- SALES FORECAST ---
if forecast_file:
    forecast = pd.read_csv(forecast_file, parse_dates=['ds'])
    st.subheader("🔮 Sales Forecast")

    fig3, ax3 = plt.subplots()
    ax3.plot(forecast['ds'], forecast['yhat'], label='Forecast')
    ax3.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3, label='Confidence Interval')
    ax3.set_title("Predicted Sales for Next 90 Days")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Revenue")
    ax3.legend()
    st.pyplot(fig3)

# --- FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ by Ayush | Streamlit Dashboard")
