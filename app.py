import streamlit as st
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="Rahuri Soil Analysis", layout="wide")

st.title("🌾 Soil Fertility and Salinity Mapping - Rahuri")
st.write("Case Study: Soil fertility mapping and fertilizer recommendation using GIS, Remote Sensing, and Machine Learning.")

# Define asset paths
assets = Path("assets")
salinity_path = assets / "salinity_map_rahuri.png"
slope_path = assets / "slope_map_rahuri.png"

# Display maps
col1, col2 = st.columns(2)
with col1:
    st.subheader("🧂 Salinity Map")
    if salinity_path.exists():
        sal_img = Image.open(salinity_path)
        st.image(sal_img, use_container_width=True)
    else:
        st.error("Salinity map not found. Please run convert_tif_to_png.py first.")

with col2:
    st.subheader("⛰️ Slope Map")
    if slope_path.exists():
        slope_img = Image.open(slope_path)
        st.image(slope_img, use_container_width=True)
    else:
        st.error("Slope map not found. Please run convert_tif_to_png.py first.")

# Footer
st.markdown("---")
st.caption("Developed for Avishkar Project — Dept. of Agricultural Engineering, Rahuri")

