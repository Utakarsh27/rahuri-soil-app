import streamlit as st
from PIL import Image
import os

# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(page_title="SmartFarm Analyzer", layout="wide")
st.title("🌾 SmartFarm Analyzer — Slope & Salinity Demo (Rahuri)")

# ---------------------------
# SIDEBAR / FARM SELECTION
# ---------------------------
st.sidebar.header("Farm Selection")
demo_farm = st.sidebar.selectbox(
    "Choose Demo Farm:",
    ["Rahuri Farm 1", "Rahuri Farm 2"]
)

st.sidebar.markdown("---")
st.sidebar.write("👩‍🌾 This demo uses pre-exported GEE maps (PNG).")

# ---------------------------
# FILE PATHS
# ---------------------------
assets_path = "assets"
sal_path_default = os.path.join(assets_path, "salinity_map_rahuri.png")
slope_path_default = os.path.join(assets_path, "slope_map_rahuri.png")

# ---------------------------
# FILE UPLOAD OPTION
# ---------------------------
st.sidebar.header("Optional: Upload your own maps")
uploaded_sal = st.sidebar.file_uploader("Upload Salinity Map (PNG)", type=["png"])
uploaded_slope = st.sidebar.file_uploader("Upload Slope Map (PNG)", type=["png"])

# ---------------------------
# LOAD IMAGES
# ---------------------------
try:
    if uploaded_sal is not None:
        sal_img = Image.open(uploaded_sal)
    else:
        sal_img = Image.open(sal_path_default)

    if uploaded_slope is not None:
        slope_img = Image.open(uploaded_slope)
    else:
        slope_img = Image.open(slope_path_default)

except FileNotFoundError as e:
    st.error(f"❌ File not found: {e}")
    st.stop()

# ---------------------------
# LAYOUT — DISPLAY MAPS
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧭 Slope Map")
    st.image(slope_img, use_container_width=True, caption="Slope Map (degrees)")

with col2:
    st.subheader("🧂 Salinity Map")
    st.image(sal_img, use_container_width=True, caption="Salinity Index")

# ---------------------------
# RECOMMENDATION
# ---------------------------
st.markdown("---")
st.subheader("💡 Recommendation Summary")

if demo_farm == "Rahuri Farm 1":
    st.info("Average slope: ~3.5% | Salinity: Moderate → Recommended crops: **Sorghum, Cotton, or Bajra**.")
else:
    st.info("Average slope: ~2% | Salinity: Low → Recommended crops: **Wheat, Maize, or Onion**.")

st.markdown("📅 *Generated using Sentinel-2 & SRTM DEM (GEE, 2024).*")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown(
    """
    <hr style="border:1px solid #ddd">
    <p style='text-align:center'>
    Built with ❤️ using Google Earth Engine, Python, and Streamlit.<br>
    <small>MPKV Rahuri — Avishkar Project 2025</small>
    </p>
    """,
    unsafe_allow_html=True
)
