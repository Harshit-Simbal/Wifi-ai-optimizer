import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from controller.wifi_controller import suggest_best_setting
from controller.inference_engine import predict_interference
from auto_detector import estimate_environment, get_wifi_scan_data
import pandas as pd
import altair as alt

st.set_page_config(page_title="AI Wi-Fi Optimizer", layout="centered")
st.title("📶 AI-Augmented Wi-Fi Interference Manager")

st.header("📡 Smart Wi-Fi Optimizer")
auto_mode = st.checkbox("🧠 Auto Detect Network Conditions", value=True)

if auto_mode:
    with st.spinner("Scanning Wi-Fi environment..."):
        try:
            devices_opt, snr_opt = estimate_environment()
            st.success(f"Detected {devices_opt} devices | Estimated SNR: {snr_opt:.1f} dB")
        except Exception as e:
            st.error(f"Auto-detection failed: {str(e)}")
            devices_opt = st.slider("Device Density", 10, 100, 30)
            snr_opt = st.slider("Signal-to-Noise Ratio (S)", 10, 50, 25)
else:
    devices_opt = st.slider("Device Density", 10, 100, 30)
    snr_opt = st.slider("Signal-to-Noise Ratio (SNR)", 10, 50, 25)

if st.button("Run Optimizer"):
    best_channel, best_power, interference = suggest_best_setting(device_density=devices_opt, signal_to_noise=snr_opt, return_result=True)
    st.success(f"✅ Best Channel: {best_channel}, Power: {best_power} dBm")
    st.info(f"Estimated Interference: {interference:.2f}")

st.header("📊 Nearby Wi-Fi Signal Strength")
wifi_data = get_wifi_scan_data()
if wifi_data:
    df = pd.DataFrame(wifi_data, columns=["SSID", "RSSI (dBm)"])
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("SSID", sort="-y"), y="RSSI (dBm)", color="SSID"
    ).properties(width=700, height=400)
    st.altair_chart(chart)
else:
    st.info("No networks found or unable to scan.")
