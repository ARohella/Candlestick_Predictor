import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Title and description
st.title("📈 TradeTorch's Stock Candlestick Predictor!")
st.write("Select a stock from the dropdown below:")

# Dropdown menu with 5 preloaded stocks
stocks = {
    "AAPL": "Apple Inc.",
    "TSLA": "Tesla Inc.",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "MSFT": "Microsoft Corp.",
    "NVDA": "NVIDIA Corp.",
    "SBUX": "Starbucks Corp.",
}

selected_stock = st.selectbox("Choose a stock:", options=list(stocks.keys()))

# Display selected stock information
if selected_stock:
    st.write(f"**Selected Stock:** {stocks[selected_stock]}")
    st.write(f"**Ticker Symbol:** {selected_stock}")

# Dropdown for time range selection
time_range = st.selectbox(
    "Select Time Range for Historical Data:",
    options=["1mo", "3mo", "6mo", "1y", "5y", "max"],
    index=3,  # Default is 1 year
)

# Add a button to navigate to stock details page
if st.button("Show Prediction!", key="prediction"):
    # Fetch stock data using Yahoo Finance API
    stock_data = yf.Ticker(selected_stock)

    # Fetch historical data based on the selected time range
    df = stock_data.history(period=time_range)

    if df.empty:
        st.error("No data available for this stock.")
    else:
        # Display the company name and ticker
        st.title(f"Details for {stocks[selected_stock]} ({selected_stock})")

        # Market summary
        open_price = stock_data.info.get("open", "N/A")
        previous_close = stock_data.info.get("previousClose", "N/A")
        day_low = stock_data.info.get("dayLow", "N/A")
        day_high = stock_data.info.get("dayHigh", "N/A")
        fifty_two_week_low = stock_data.info.get("fiftyTwoWeekLow", "N/A")
        fifty_two_week_high = stock_data.info.get("fiftyTwoWeekHigh", "N/A")
        volume = stock_data.info.get("volume", "N/A")
        avg_volume = stock_data.info.get("averageVolume", "N/A")

        # Market summary
        st.write("### Market Summary:")

        # Create two columns for the market summary
        col1, col2, col3 = st.columns([0.35, 0.5, 0.3])

        # Left column data
        with col1:
            metrics = {
                "Open Price": f"${open_price}",
                "Previous Close": f"${previous_close}",
            }
            for label, value in metrics.items():
                st.metric(label=label, value=value)

        # Right column data
        with col2:
            metrics = {
                "Day's Range": f"${day_low} - ${day_high}",
                "52-Week Range": f"${fifty_two_week_low} - ${fifty_two_week_high}",
            }
            for label, value in metrics.items():
                st.metric(label=label, value=value)

        with col3:
            metrics = {
                "Volume": f"{volume:,}",
                "Average Volume (3M)": f"{avg_volume:,}"
            }
            for label, value in metrics.items():
                st.metric(label=label, value=value)

        # Candlestick chart with full historical data
        st.write("### Candlestick Chart:")
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                )
            ]
        )
        fig.update_layout(
            title=f"Candlestick Chart for {selected_stock} ({time_range} Range)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=True,  # Enables the range slider for zooming
        )
        st.plotly_chart(fig)
