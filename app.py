# app.py

import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Ratio-BB Strategy Inspector")

# Sidebar parameters
window = st.sidebar.slider("BB Window (periods)", 5, 50, 20)
stddev = st.sidebar.slider("StdDev Factor", 1.0, 3.0, 2.0)

uploaded = st.file_uploader("Upload ticks JSON", type="json")
if not uploaded:
    st.info("Upload een JSON-bestand met ticks om te starten.")
    st.stop()

# Lees ticks in
df = pd.read_json(uploaded)
df['time'] = pd.to_datetime(df['timestamp'], unit='s')
df = df.set_index('time').sort_index()

# Bollinger Bands
df['sma'] = df['price'].rolling(window).mean()
df['std'] = df['price'].rolling(window).std()
df['upper'] = df['sma'] + stddev * df['std']
df['lower'] = df['sma'] - stddev * df['std']

# Ratios
df['ratio_lower'] = df['price'] / df['lower']
df['ratio_upper'] = df['price'] / df['upper']

# Bepaal laatste signaal
last = df.iloc[-1]
if last['ratio_lower'] < 1.0:
    signal = "SWAP_TFUEL_TO_THETA"
elif last['ratio_upper'] > 1.0:
    signal = "SWAP_THETA_TO_TFUEL"
else:
    signal = "NO_SWAP"

st.subheader("Latest Signal")
st.write(signal)

st.subheader("Price & Bollinger Bands")
st.line_chart(df[['price','sma','upper','lower']])

st.subheader("Detailed Data")
st.dataframe(df[['price','ratio_lower','ratio_upper']])

st.markdown("""
Run met:
```
streamlit run app.py
```
Upload je ticks.JSON en speel met de sliders om het effect te zien.
""")