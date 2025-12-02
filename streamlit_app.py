# ----------------------------------------------------------
# 🌾 Crop Yield & Production Prediction App (Premium UI 2025)
# ----------------------------------------------------------

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import altair as alt

# MODEL PATH
MODEL_PATH = Path("decision_tree_pipeline.joblib")

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="🌾 Crop Yield Predictor", layout="wide")

# ----------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: #0e1929;
    color: white !important;
}

/* Main heading */
.big-title {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    padding: 15px;
    color: #1abc9c;
}

/* Section titles */
.section-title {
    font-size: 26px;
    color: #38b2ac;
    font-weight: 700;
    margin-bottom: 12px;
    margin-top: 8px;
}

/* Remove cards (no background boxes) */
.card {
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* Increase font size of form labels */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
}

/* Prediction result card */
.result-card {
    background: #e6fff7;
    padding: 25px;
    border-radius: 15px;
    border-left: 7px solid #00a389;
    color: #0a3d3a;
    font-size: 22px;
    font-weight: 600;
    margin-top: 20px;
}

/* Metric cards */
.metric-card {
    background: #1a2e47;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    color: #9ae6b4;
    box-shadow: 0 0 15px rgba(0,255,180,0.15);
}

/* Predict Button */
.stButton>button {
    background: linear-gradient(90deg, #1abc9c, #149174);
    color: white;
    padding: 12px 26px;
    border-radius: 10px;
    font-size: 20px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #149174, #0f7158);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
st.markdown("<div class='big-title'>🌾 ML Based Crop Yield & Production Predictor</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# Load Model
# ----------------------------------------------------------
@st.cache_resource
def load_model():
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except:
            st.error("⚠️ Model found but could not be loaded.")
            return None
    else:
        st.warning("⚠️ No model found — Running in DEMO MODE.")
        return None

model = load_model()

# ----------------------------------------------------------
# Dropdown Data
# ----------------------------------------------------------
STATE_DISTRICTS = {
    "Andaman and Nicobar Islands": ["NICOBARS","NORTH AND MIDDLE ANDAMAN","SOUTH ANDAMANS"],
    "Andhra Pradesh": ["ANANTAPUR","CHITTOOR","EAST GODAVARI","GUNTUR","KADAPA","KRISHNA","KURNOOL",
                       "PRAKASAM","SPSR NELLORE","SRIKAKULAM","VISAKHAPATANAM","VIZIANAGARAM","WEST GODAVARI"],
    "Assam": ["BAKSA","BARPETA","BONGAIGAON","CACHAR","CHIRANG","DARRANG"],
    "Bihar": ["ARARIA","ARWAL","AURANGABAD","BANKA","BEGUSARAI"],
}

SEASONS = ["Kharif","Rabi","Whole Year","Autumn","Summer","Winter"]

CROPS = [
    'Rice','Wheat','Banana','Coconut','Maize','Sugarcane','Potato','Turmeric',
    'Groundnut','Blackgram','Peas','Onion','Tomato','Paddy'
]

# ----------------------------------------------------------
# TWO PANEL LAYOUT
# ----------------------------------------------------------
left, right = st.columns([1,1])

# ----------------------------------------------------------
# LEFT PANEL — LOCATION & CROP DETAILS
# ----------------------------------------------------------
with left:
    st.markdown("<div class='section-title'>📍 Enter Location & Crop Details</div>", unsafe_allow_html=True)

    state = st.selectbox("State", list(STATE_DISTRICTS.keys()))
    district = st.selectbox("District", STATE_DISTRICTS[state])
    crop = st.selectbox("Crop", CROPS)
    season = st.selectbox("Season", SEASONS)
    year = st.number_input("Crop Year", 1990, 2050, 2025)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# RIGHT PANEL — ENVIRONMENT INPUTS
# ----------------------------------------------------------
with right:
    st.markdown("<div class='section-title'>🌡️ Environment Inputs</div>", unsafe_allow_html=True)

    temp = st.slider("Temperature (°C)", 10, 50, 30)
    hum = st.slider("Humidity (%)", 10, 100, 50)
    soil = st.slider("Soil Moisture (%)", 0, 100, 45)
    area = st.number_input("Cultivation Area (Units)", 0.1, 100000.0, 100.0)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# Predict Button (Centered)
# ----------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
center = st.columns([3,2,3])
with center[1]:
    predict = st.button("🚀 Predict Yield & Production")

# ----------------------------------------------------------
# RESULT SECTION
# ----------------------------------------------------------
if predict:
    row = {
        "State_Name": state,
        "District_Name": district,
        "Crop_Year": str(year),
        "Season": season,
        "Crop": crop,
        "Temperature": temp,
        "Humidity": hum,
        "Soil_Moisture": soil,
        "Area": area
    }

    df_in = pd.DataFrame([row])

    if model:
        pred_yield = float(model.predict(df_in)[0])
    else:
        pred_yield = (temp * 0.02) + (soil * 0.01)  # DEMO MODE

    prod = pred_yield * area

    st.markdown(f"""
        <div class="result-card">
            🌱 Predicted Yield: <b>{pred_yield:.3f}</b> per unit <br><br>
            📦 Total Production: <b>{prod:.2f}</b> units <br><br>
        </div>
    """, unsafe_allow_html=True)

    # EXTRA METRICS
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'>🌡️ Temp Score:<br><b>{temp*2}%</b></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'>💧 Moisture Index:<br><b>{soil*1.5}</b></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'>☁️ Humidity Factor:<br><b>{hum*1.2}</b></div>", unsafe_allow_html=True)

    # OPTIONAL — YEARWISE CHART (DEMO CHART)
    chart_df = pd.DataFrame({
        "Year": [year-2, year-1, year, year+1],
        "Production": [prod*0.7, prod*0.85, prod, prod*1.1]
    })

    line = alt.Chart(chart_df).mark_line(point=True, color="#1abc9c").encode(
        x="Year:O", y="Production:Q"
    ).properties(title="📈 Estimated Production Trend", height=350)

    st.altair_chart(line, use_container_width=True)

# ----------------------------------------------------------
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit | Atanu Paul")


