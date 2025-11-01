import streamlit as st
from PIL import Image
import pandas as pd

# -----------------------------------------------------------
# SMARTFARM ANALYZER — MPKV RAHURI DEMO (Slope & Salinity)
# -----------------------------------------------------------

st.set_page_config(page_title="SmartFarm Analyzer", layout="wide")

st.title("🌾 SmartFarm Analyzer — Soil Salinity & Slope (MPKV Rahuri)")
st.markdown("### A simple decision support demo using Google Earth Engine outputs")

# Sidebar: Select Farm / Area
st.sidebar.header("Select Demo Farm / Area")
selected_farm = st.sidebar.selectbox(
    "Choose a farm or area",
    ("Rahuri Block - Demo 1", "Rahuri Block - Demo 2")
)

# Sidebar: Basic info
st.sidebar.markdown("**Note:** These maps are derived from Sentinel-2 & SRTM data (2024).")
st.sidebar.markdown("Salinity = proxy index from NDVI + NDWI (not lab EC values).")

# Load exported PNGs from GEE (keep them in ./assets/)
sal_img = Image.open("assets/salinity_map_rahuri.png")
slope_img = Image.open("assets/slope_map_rahuri.png")

# Layout columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧭 Slope Map")
    st.image(slope_img, use_container_width=True)
    st.caption("Data source: SRTM (30 m) DEM")

with col2:
    st.subheader("🧂 Soil Salinity Proxy Map")
    st.image(sal_img, use_container_width=True)
    st.caption("Computed from Sentinel-2 NDVI + NDWI indices (2024 median composite)")

# Recommendation logic (very simple rule)
st.markdown("---")
st.subheader("📋 Crop Recommendation")

# Example lookup table (you can load from CSV if you like)
crop_lookup = pd.DataFrame({
    "Crop": ["Wheat", "Sorghum", "Cotton", "Rice", "Bajra"],
    "MaxSlope": [3, 8, 6, 2, 10],
    "MaxSalinityClass": [1, 2, 3, 1, 3],
    "Note": [
        "Needs low salinity and gentle slope",
        "Moderate salinity tolerant",
        "Tolerates higher salinity",
        "Requires low slope and low salinity",
        "Tolerant to salinity and slope"
    ]
})

# Example values — in a real version you can compute from your map stats
avg_slope = 5.2
salinity_class = 2   # 1=low, 2=moderate, 3=high

recommended = crop_lookup[
    (crop_lookup["MaxSlope"] >= avg_slope) &
    (crop_lookup["MaxSalinityClass"] >= salinity_class)
]["Crop"].tolist()

if len(recommended) > 0:
    st.success(
        f"**Average slope:** {avg_slope:.1f}%  |  **Salinity:** Moderate (Class {salinity_class})  \n\n"
        f"✅ Suitable crops: {', '.join(recommended)}"
    )
else:
    st.warning(
        f"Average slope: {avg_slope:.1f}%  |  Salinity: Moderate (Class {salinity_class})  \n"
        f"No crops found meeting both criteria."
    )

st.markdown("*(Prototype: For field validation, compare with soil EC tests or soil health cards.)*")
