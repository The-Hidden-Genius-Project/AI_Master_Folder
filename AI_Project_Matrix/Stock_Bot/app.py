import requests
import numpy as np
import matplotlib.pyplot as plt

# Function to fetch stock data from Alpha Vantage API
def fetch_stock_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['Time Series (Daily)']

# Function to calculate moving average
def calculate_moving_average(data, window_size=20):
    closes = [float(data[date]['4. close']) for date in sorted(data.keys())]
    return np.convolve(closes, np.ones(window_size)/window_size, mode='valid')

# Function to make trading decisions based on moving averages
def make_trading_decision(moving_average_short, moving_average_long):
    if moving_average_short[-1] > moving_average_long[-1]:
        return 'BUY'
    elif moving_average_short[-1] < moving_average_long[-1]:
        return 'SELL'
    else:
        return 'HOLD'

if __name__ == "__main__":
    symbol = ''  # Example stock symbol (Apple Inc.)
    api_key = 'KMVOFO8HVNEGR81M'  # Replace with your API key

    data = fetch_stock_data(symbol, api_key)

    # Calculate moving averages
    moving_average_short = calculate_moving_average(data, window_size=50)
    moving_average_long = calculate_moving_average(data, window_size=200)

    # Make trading decision
    decision = make_trading_decision(moving_average_short, moving_average_long)
    print(f"Trading decision for {symbol}: {decision}")

    # Plotting
    dates = sorted(data.keys())
    closes = np.array([float(data[date]['4. close']) for date in dates])

    # Ensure all arrays have the same length
    min_length = min(len(dates), len(moving_average_short), len(moving_average_long))
    dates = dates[-min_length:]
    closes = closes[-min_length:]
    moving_average_short = moving_average_short[-min_length:]
    moving_average_long = moving_average_long[-min_length:]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, moving_average_short, label='50-Day Moving Average', color='red')
    plt.plot(dates, moving_average_long, label='200-Day Moving Average', color='blue')
    plt.plot(dates, closes, label='Closing Price', color='green')
    plt.title(f"Stock Price and Moving Averages for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
