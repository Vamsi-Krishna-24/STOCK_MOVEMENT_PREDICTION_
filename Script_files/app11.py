import pickle 
import pandas as pd
import streamlit as st
import yfinance as yf
import os

# Load the trained model
file_path = '/Users/surisettivamsikrishna/Downloads/FInal Projects/MarketMastery-Predictive-Analysis/ML_Algo/random_forest_model.pkl'
if os.path.exists(file_path):
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
else:
    st.error(f"The file {file_path} does not exist.")

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
    sell_button_html = '<button style="background-color: red; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">SELL</button>'
    if st.markdown(sell_button_html, unsafe_allow_html=True):
        st.error("Trade Recommendation: SELL")
else:
    buy_button_html = '<button style="background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">BUY</button>'
    if st.markdown(buy_button_html, unsafe_allow_html=True):
        st.success("Trade Recommendation: BUY")

# Streamlit app for visualizing historical data (optional)
# Importing the data through yfinance library
nse = yf.Ticker("^NSEI")
nse = nse.history(period="max")

# Chart of NSE
st.subheader("Historical Data Visualization")
st.line_chart(nse['Close'])


