import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- 1. CPR & PIVOT CALCULATION ENGINE ---
def calculate_pivots(high, low, close):
    p = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (p - bc) + p
    
    h_l_diff = high - low
    levels = {
        "TC": round(tc, 2), "P": round(p, 2), "BC": round(bc, 2),
        "R1": round((2 * p) - low, 2), "S1": round((2 * p) - high, 2),
        "R2": round(p + h_l_diff, 2), "S2": round(p - h_l_diff, 2),
        "R3": round(high + 2 * (p - low), 2), "S3": round(low - 2 * (high - p), 2),
        "R4": round((high + 2 * (p - low)) + h_l_diff, 2), 
        "S4": round((low - 2 * (high - p)) - h_l_diff, 2)
    }
    return levels

# --- 2. UI SETUP ---
st.set_page_config(page_title="Nifty CPR Dashboard", layout="wide")
st.title("📊 Nifty CPR & Strategy Builder")

# Sidebar for Market Inputs
st.sidebar.header("Previous Day OHLC")
prev_high = st.sidebar.number_input("Prev High", value=24253.80)
prev_low = st.sidebar.number_input("Prev Low", value=24126.65)
prev_close = st.sidebar.number_input("Prev Close", value=24176.15)
spot_price = st.sidebar.number_input("Current Nifty Spot", value=prev_close)

levels = calculate_pivots(prev_high, prev_low, prev_close)

# --- 3. THREE-TABLE LAYOUT ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Central Pivot Range")
    st.markdown(f"""
    | Level | Value |
    | :--- | :--- |
    | **TC** | **{levels['TC']}** |
    | **Pivot (P)** | **{levels['P']}** |
    | **BC** | **{levels['BC']}** |
    """)
    width = round(abs(levels['TC'] - levels['BC']), 2)
    st.info(f"Width: {width} ({'Narrow' if width < 15 else 'Wide'})")

with col2:
    st.subheader("Resistance Levels")
    st.markdown(f"""
    | Level | Value |
    | :--- | :--- |
    | **R4** | {levels['R4']} |
    | **R3** | {levels['R3']} |
    | **R2** | {levels['R2']} |
    | **R1** | {levels['R1']} |
    """)

with col3:
    st.subheader("Support Levels")
    st.markdown(f"""
    | Level | Value |
    | :--- | :--- |
    | **S1** | {levels['S1']} |
    | **S2** | {levels['S2']} |
    | **S3** | {levels['S3']} |
    | **S4** | {levels['S4']} |
    """)

st.divider()

# --- 4. CHARTING ---
fig = go.Figure()
fig.add_hline(y=spot_price, line_color="yellow", line_width=2, annotation_text="SPOT")
fig.add_hrect(y0=min(levels['TC'], levels['BC']), y1=max(levels['TC'], levels['BC']), 
              fillcolor="rgba(255,255,255,0.1)", line_width=0)

for name, val in levels.items():
    color = "red" if "R" in name else "green" if "S" in name else "white"
    fig.add_hline(y=val, line_dash="dot", line_color=color, annotation_text=name)

fig.update_layout(template="plotly_dark", height=600)
st.plotly_chart(fig, use_container_width=True)
