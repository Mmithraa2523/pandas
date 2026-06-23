import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="HCLTECH Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 HCLTECH Stock Analytics Dashboard")

# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv("gold/hcltech.csv")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# -------------------------
# SIDEBAR FILTER
# -------------------------

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# -------------------------
# KPI CARDS
# -------------------------

st.subheader("Key Metrics")

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

# -------------------------
# STOCK PRICE TREND
# -------------------------

st.subheader("Closing Price Trend")

fig = px.line(
    filtered_df,
    x="Date",
    y="Close"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------
# MOVING AVERAGE
# -------------------------

st.subheader("Moving Average Analysis")

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

# -------------------------
# VOLUME ANALYSIS
# -------------------------

st.subheader("Trading Volume")

fig_volume = px.bar(
    filtered_df,
    x="Date",
    y="Volume"
)

st.plotly_chart(
    fig_volume,
    use_container_width=True
)

# -------------------------
# DAILY RETURN
# -------------------------

st.subheader("Daily Return %")

fig_return = px.line(
    filtered_df,
    x="Date",
    y="Daily_return"
)

st.plotly_chart(
    fig_return,
    use_container_width=True
)

# -------------------------
# VOLATILITY
# -------------------------

st.subheader("Volatility %")

fig_volatility = px.line(
    filtered_df,
    x="Date",
    y="Volatility_%"
)

st.plotly_chart(
    fig_volatility,
    use_container_width=True
)

# -------------------------
# TREND DISTRIBUTION
# -------------------------

st.subheader("Trend Distribution")

trend_count = filtered_df["Trend"].value_counts()

fig_pie = px.pie(
    values=trend_count.values,
    names=trend_count.index
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# -------------------------
# CORRELATION MATRIX
# -------------------------

st.subheader("Correlation Matrix")

corr_cols = [
    "Close",
    "Volume",
    "Daily_return",
    "Price_Range",
    "Volatility_%"
]

corr = filtered_df[corr_cols].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# -------------------------
# DATA TABLE
# -------------------------

st.subheader("Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -------------------------
# DOWNLOAD BUTTON
# -------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_hcltech.csv",
    "text/csv"
)