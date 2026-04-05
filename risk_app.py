import streamlit as st
import plotly.graph_objects as go

# --- APP CONFIG ---
st.set_page_config(page_title="Chemical Risk Dashboard", layout="centered")

st.title("🧪 Chemical Risk Calculator")
st.markdown("Adjust the concentration levels and thresholds to see the real-time Risk Score.")

# --- SIDEBAR: THRESHOLDS ---
st.sidebar.header("Set Normal Ranges (Thresholds)")
st_limit = st.sidebar.number_input("Styrene Limit", value=50)
al_limit = st.sidebar.number_input("Alkanes Limit", value=100)
de_limit = st.sidebar.number_input("Decanal Limit", value=20)
pr_limit = st.sidebar.number_input("2-Propanone Limit", value=200)

# --- MAIN PANEL: INPUTS ---
col1, col2 = st.columns(2)

with col1:
    styrene = st.slider("Styrene Level", 0, 200, 25)
    alkanes = st.slider("Alkanes Level", 0, 500, 80)
with col2:
    decanal = st.slider("Decanal Level", 0, 100, 10)
    propanone = st.slider("2-Propanone Level", 0, 1000, 150)

# --- LOGIC: CALCULATION ---
# Simple logic: (Current / Limit) * weighted factor
# We'll normalize this to a 0-100 scale
total_ratio = (styrene/st_limit + alkanes/al_limit + decanal/de_limit + propanone/pr_limit) / 4
risk_score = min(int(total_ratio * 50), 100) # Scaling factor of 50 for sensitivity

# Determine Label and Color
if risk_score < 20:
    label, color = "Low", "blue"
elif risk_score < 40:
    label, color = "Moderate", "green"
elif risk_score < 60:
    label, color = "High", "gold"
elif risk_score < 80:
    label, color = "Very High", "orange"
else:
    label, color = "Critical", "red"

# --- VISUALIZATION: GAUGE CHART ---
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = risk_score,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': f"Current Risk: {label}", 'font': {'size': 24, 'color': color}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1},
        'bar': {'color': "black"},
        'steps': [
            {'range': [0, 20], 'color': "#E8F4F8"},
            {'range': [20, 40], 'color': "#90EE90"},
            {'range': [40, 60], 'color': "#FFD700"},
            {'range': [60, 80], 'color': "#FF8C00"},
            {'range': [80, 100], 'color': "#FF0000"}
        ],
    }
))

fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# --- DATA SUMMARY ---
st.info(f"The score is calculated based on current levels relative to your set limits.")