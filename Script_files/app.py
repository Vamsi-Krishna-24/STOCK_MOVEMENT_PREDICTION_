# Importing necessary libraries
import yfinance as yf
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

# Importing the data through yfinance library
nse = yf.Ticker("^NSEI")
nse = nse.history(period="max")

# Importing the data through yfinance library
nse = yf.Ticker("^NSEI")
nse = nse.history(period="max")

# Feature Engineering
if 'Dividends' in nse.columns:
    del nse['Dividends']
if 'Stock Splits' in nse.columns:
    del nse['Stock Splits']

nse["tomorrow"] = nse["Close"].shift(-1)
nse["target"] = (nse["tomorrow"] > nse["Close"]).astype(int)


# Creating RandomForestClassifier model
model = RandomForestClassifier(n_estimators=200, min_samples_split=100, random_state=1)

# Splitting the data into train and test sets
train = nse.iloc[:-100]
test = nse.iloc[-100:]

# Defining features (x) and target (y)
x = ["Close", "Open", "High", "Low", "Volume"]
y = "target"

# Fitting the model
model.fit(train[x], train[y])

# Function to make predictions
def predict(train, test, x, model):
    model.fit(train[x], train["target"])
    preds = model.predict(test[x])
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["target"], preds], axis=1)
    return combined

# Function for backtesting
def backtest(data, model, x, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i + step)].copy()
        predictions = predict(train, test, x, model)
        all_predictions.append(predictions)

    return pd.concat(all_predictions)

# Running backtest
predictions = backtest(nse, model, x)

# Streamlit app
st.title("Stock Price Prediction App")

# Sidebar with user input
st.sidebar.header("User Input")

user_close = st.sidebar.number_input("Enter the closing price:")
user_open = st.sidebar.number_input("Enter the opening price:")
user_high = st.sidebar.number_input("Enter the high price:")
user_low = st.sidebar.number_input("Enter the low price:")
user_volume = st.sidebar.number_input("Enter the volume:")

# Display user input
st.sidebar.subheader("User Input:")
user_data = pd.DataFrame({
    'Close': [user_close],
    'Open': [user_open],
    'High': [user_high],
    'Low': [user_low],
    'Volume': [user_volume]
})
st.sidebar.write(user_data)

# Make predictions using the trained model
prediction = model.predict(user_data)[0]

# Display predictions
st.subheader("Predictions:")

# Display the Buy/Sell buttons with HTML and CSS for color
if prediction == 0:
    st.error("Trade Recommendation: SELL")
else:
    st.success("Trade Recommendation: BUY")

# Streamlit app for visualizing historical data (optional)
# Importing the data through yfinance library
nse = yf.Ticker("^NSEI")
nse = nse.history(period="max")

# Chart of NSE
st.subheader("Historical Data Visualization")
st.line_chart(nse['Close'])




