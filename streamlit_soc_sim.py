import streamlit as st
import numpy as np
import pandas as pd
import joblib
import time

# Load trained model
import joblib
import urllib.request
import os

# File path and Google Drive link
model_path = "model.pkl"
drive_file_id = "1ZJVlr5JZUhvIYVGwlcdlfFXdjsVO7akA"
url = f"https://drive.google.com/uc?id={drive_file_id}"

# Download the model if not already downloaded
if not os.path.exists(model_path):
    urllib.request.urlretrieve(url, model_path)

# Load model
model = joblib.load(model_path)


# Page configuration
st.set_page_config(page_title="SoC Simulator", layout="centered")
st.title("🔋 SoC Simulator")
st.subheader("⚙️ Input Parameters")

# Initialize voltage state
if 'voltage_level' not in st.session_state:
    st.session_state.voltage_level = 3.7  # Starting nominal voltage

# Simulation mode toggle
simulate = st.checkbox("🔁 Enable Auto Simulation", value=True)

# Input generation
if simulate:
    current = round(np.random.uniform(-3.0, 2.0), 2)

    if current > 0:
        st.session_state.voltage_level = min(st.session_state.voltage_level + 0.005, 4.2)
    elif current < 0:
        st.session_state.voltage_level = max(st.session_state.voltage_level + (current * 0.01), 3.2)

    voltage = round(st.session_state.voltage_level, 2)
    temperature = round(np.random.uniform(-20, 25), 1)
    time.sleep(1)

else:
    col1, col2 = st.columns(2)

    with col1:
        voltage = st.slider("🔌 Voltage (V)", 3.2, 4.2, 3.7, 0.01)
        temperature = st.slider("🌡️ Temperature (°C)", -20.0, 25.0, 0.0, 1.0)

    with col2:
        current = st.slider("⚡ Current (A)", -3.0, 2.0, -1.0, 0.01)

# Charging/Discharging/Idle state
charge_state = "⚡ Charging" if current > 0 else "🔋 Discharging" if current < 0 else "⏸️ Idle"
state_color = "green" if current > 0 else "red" if current < 0 else "gray"

# Predict SoC
df = pd.DataFrame({"Voltage": [voltage], "Current": [current], "Temp": [temperature]})
predicted_soc = model.predict(df)[0]

# Display results
st.metric("📊 Estimated SoC", f"{predicted_soc:.2f}%")
st.markdown(f"""
<h3 style='color:{state_color}; text-align: center'>
    {charge_state}
</h3>
""", unsafe_allow_html=True)

# Show input data
st.write("**Current Input Values:**")
st.dataframe(df)

# History and chart
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Voltage", "Current", "Temp", "SoC"])

new_row = {"Voltage": voltage, "Current": current, "Temp": temperature, "SoC": predicted_soc}
st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True)

st.subheader("📈 SoC Estimation Graph")
st.line_chart(st.session_state.history[["SoC"]])

# Footer
st.markdown("---")
st.caption("👩‍💻 Developed by Bengu Beyza Kapan | Real-Time SoC Estimation using Machine Learning")
