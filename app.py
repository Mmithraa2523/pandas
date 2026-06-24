import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HCLTECH Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.metric-container {
    background-color: #f5f5f5;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #ddd;
}

h1 {
    text-align: center;
}

div[data-testid="stMetric"] {
    background-color: #222222;
    border: 1px solid #e6e6e6;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<h1>📈 HCLTECH Stock Analytics Dashboard</h1>
<p style='text-align:center;color:gray;'>
Interactive Dashboard using Streamlit & Plotly
</p>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("gold/hcltech.csv")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    return df

df = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📊 Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date))
    &
    (df["Date"] <= pd.to_datetime(end_date))
]

# ==========================================
# KPI CARDS
# ==========================================

st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Close Price",
        f"₹{filtered_df['Close'].iloc[-1]}"
    )

with col2:
    st.metric(
        "Highest Price",
        f"₹{filtered_df['High'].max()}"
    )

with col3:
    st.metric(
        "Lowest Price",
        f"₹{filtered_df['Low'].min()}"
    )

with col4:
    st.metric(
        "Average Volume",
        f"{int(filtered_df['Volume'].mean()):,}"
    )

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "📈 Analysis",
        "📄 Dataset"
    ]
)

# ==========================================
# OVERVIEW TAB
# ==========================================

with tab1:

    st.subheader("📈 Closing Price Trend")

    fig_close = px.line(
        filtered_df,
        x="Date",
        y="Close",
        title="Closing Price Trend"
    )

    fig_close.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_close,
        use_container_width=True
    )

    st.subheader("📊 Trend Distribution")

    trend_count = filtered_df["Trend"].value_counts()

    fig_pie = px.pie(
        values=trend_count.values,
        names=trend_count.index,
        hole=0.4
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

    uptrend = (filtered_df["Trend"] == "Uptrend").sum()
    downtrend = (filtered_df["Trend"] == "Downtrend").sum()

    st.success(
        f"📈 Uptrend Days: {uptrend} | 📉 Downtrend Days: {downtrend}"
    )

# ==========================================
# ANALYSIS TAB
# ==========================================

with tab2:

    # Moving Average

    st.subheader("📈 Moving Average Analysis")

    fig_ma = go.Figure()

    fig_ma.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Close"],
            name="Close Price"
        )
    )

    fig_ma.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Ma_5day"],
            name="5 Day MA"
        )
    )

    fig_ma.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Ma_20day"],
            name="20 Day MA"
        )
    )

    st.plotly_chart(
        fig_ma,
        use_container_width=True
    )

    # Volume

    st.subheader("📦 Trading Volume")

    fig_volume = px.bar(
        filtered_df,
        x="Date",
        y="Volume"
    )

    st.plotly_chart(
        fig_volume,
        use_container_width=True
    )

    # Daily Return

    st.subheader("💹 Daily Return (%)")

    fig_return = px.line(
        filtered_df,
        x="Date",
        y="Daily_return"
    )

    st.plotly_chart(
        fig_return,
        use_container_width=True
    )

    # Volatility

    st.subheader("⚡ Volatility (%)")

    fig_volatility = px.line(
        filtered_df,
        x="Date",
        y="Volatility_%"
    )

    st.plotly_chart(
        fig_volatility,
        use_container_width=True
    )


# ==========================================
# DATASET TAB
# ==========================================

with tab3:

    st.subheader("📄 Gold Layer Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Filtered Dataset",
        data=csv,
        file_name="hcltech_filtered_data.csv",
        mime="text/csv"
    )



