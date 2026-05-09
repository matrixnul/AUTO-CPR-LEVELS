import streamlit as st

# --- 1. CPR & PIVOT CALCULATION ENGINE ---
def calculate_pivots(high, low, close):
    p = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (p - bc) + p
    h_l_diff = high - low
    return {
        "TC": round(tc, 2), "P": round(p, 2), "BC": round(bc, 2),
        "R1": round((2 * p) - low, 2), "S1": round((2 * p) - high, 2),
        "R2": round(p + h_l_diff, 2), "S2": round(p - h_l_diff, 2),
        "R3": round(high + 2 * (p - low), 2), "S3": round(low - 2 * (high - p), 2),
        "R4": round((high + 2 * (p - low)) + h_l_diff, 2), 
        "S4": round((low - 2 * (high - p)) - h_l_diff, 2)
    }

# --- 2. UI CONFIG & STYLING ---
st.set_page_config(page_title="Nifty CPR Dashboard", layout="wide")

st.markdown("""
    <style>
    .level-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .cpr-card { background-color: #f8f9fa; border-left: 6px solid #5758bb; }
    .res-card { background-color: #fffafa; border-left: 6px solid #eb4d4b; }
    .sup-card { background-color: #f7fff7; border-left: 6px solid #6ab04c; }
    .label { font-size: 1rem; color: #4b4b4b; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; }
    .value { font-size: 1.8rem; color: #1e272e; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("Market Data Inputs")
prev_high = st.sidebar.number_input("Prev Day High", value=24253.80)
prev_low = st.sidebar.number_input("Prev Day Low", value=24126.65)
prev_close = st.sidebar.number_input("Prev Day Close", value=24176.15)

levels = calculate_pivots(prev_high, prev_low, prev_close)
width = round(abs(levels['TC'] - levels['BC']), 2)

st.title("📊 Nifty CPR Dashboard")

# --- 3. CPR SECTION ---
st.subheader("Central Pivot Range")
c1, c2, c3, c4 = st.columns(4)

with c1: st.markdown(f'<div class="level-card cpr-card"><div class="label">TC</div><div class="value">{levels["TC"]}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="level-card cpr-card"><div class="label">PIVOT (P)</div><div class="value">{levels["P"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="level-card cpr-card"><div class="label">BC</div><div class="value">{levels["BC"]}</div></div>', unsafe_allow_html=True)
with c4:
    color = "#eb4d4b" if width < 15 else "#1e272e"
    st.markdown(f'<div class="level-card cpr-card"><div class="label">WIDTH</div><div class="value" style="color:{color}">{width}</div></div>', unsafe_allow_html=True)

st.divider()

# --- 4. RESISTANCE & SUPPORT GRID ---
col_r, col_s = st.columns(2)

with col_r:
    st.markdown("### 🔴 Resistance Levels")
    r1, r2 = st.columns(2)
    r1.markdown(f'<div class="level-card res-card"><div class="label">R1</div><div class="value" style="color:#eb4d4b">{levels["R1"]}</div></div>', unsafe_allow_html=True)
    r2.markdown(f'<div class="level-card res-card"><div class="label">R2</div><div class="value" style="color:#eb4d4b">{levels["R2"]}</div></div>', unsafe_allow_html=True)
    r1.markdown(f'<div class="level-card res-card"><div class="label">R3</div><div class="value" style="color:#eb4d4b">{levels["R3"]}</div></div>', unsafe_allow_html=True)
    r2.markdown(f'<div class="level-card res-card"><div class="label">R4</div><div class="value" style="color:#eb4d4b">{levels["R4"]}</div></div>', unsafe_allow_html=True)

with col_s:
    st.markdown("### 🟢 Support Levels")
    s1, s2 = st.columns(2)
    s1.markdown(f'<div class="level-card sup-card"><div class="label">S1</div><div class="value" style="color:#6ab04c">{levels["S1"]}</div></div>', unsafe_allow_html=True)
    s2.markdown(f'<div class="level-card sup-card"><div class="label">S2</div><div class="value" style="color:#6ab04c">{levels["S2"]}</div></div>', unsafe_allow_html=True)
    s1.markdown(f'<div class="level-card sup-card"><div class="label">S3</div><div class="value" style="color:#6ab04c">{levels["S3"]}</div></div>', unsafe_allow_html=True)
    s2.markdown(f'<div class="level-card sup-card"><div class="label">S4</div><div class="value" style="color:#6ab04c">{levels["S4"]}</div></div>', unsafe_allow_html=True)
