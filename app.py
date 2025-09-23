import streamlit as st
import cv2
import pytesseract
from PIL import Image
import requests
import numpy as np
import shutil
import os
import re

# -------------------------------
# Configure Tesseract Path
# -------------------------------
tesseract_path = shutil.which("tesseract")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(win_path):
        pytesseract.pytesseract.tesseract_cmd = win_path
    else:
        st.error("Tesseract OCR not found! Please install it.")
        st.stop()

# -------------------------------
# Streamlit Page Settings
# -------------------------------
st.set_page_config(page_title="Image Data Extract & Compare", layout="wide")
st.title("📷 Image Data Extract & Compare")
st.write("Upload an image OR take a photo, extract temperature text, and compare with OpenWeather API.")

# -------------------------------
# Step 1: Tabs for Upload vs Camera
# -------------------------------
tab1, tab2 = st.tabs(["📤 Upload Image", "📸 Take Photo"])

uploaded_file = None
camera_file = None

with tab1:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

with tab2:
    camera_file = st.camera_input("Click below to open your camera and take a photo")

# Pick whichever provided
image_file = uploaded_file if uploaded_file is not None else camera_file

# -------------------------------
# Step 2: OCR Extraction
# -------------------------------
extracted_temp = None

if image_file is not None:
    image = Image.open(image_file).convert("RGB")
    img_array = np.array(image)

    st.image(image, caption="Selected Image", use_column_width=True)

    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    extracted_text = pytesseract.image_to_string(gray)

    st.subheader("📝 Extracted Text")
    st.text(extracted_text)

    # Regex for temperature (integer or fractional, like 28, 28.5, 28°C)
    temp_matches = re.findall(r'(\d+\.?\d*)\s*(?:°|°C|degree|degrees)', extracted_text, flags=re.IGNORECASE)
    if temp_matches:
        extracted_temp = int(round(float(temp_matches[0])))
        st.success(f"Extracted Temperature: {extracted_temp}°C")
    else:
        st.warning("⚠️ No valid temperature value detected.")

# -------------------------------
# Step 3: API Compare
# -------------------------------
city = st.text_input("Enter city name for weather check", "Dhaka")

if st.button("Compare with API"):
    api_key = "22f9ea86b3c7d79c4a1df5b7a06da497"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("main"):
            api_temp = round(data["main"]["temp"])
            st.info(f"🌤 Current API Temperature in {city}: {api_temp}°C")

            if extracted_temp is not None:
                if extracted_temp == api_temp:
                    st.success("✅ Match! Extracted temperature matches API data.")
                else:
                    st.error("❌ Not Match! Extracted temperature does not match API data.")
            else:
                st.error("❌ Not Match! No temperature value detected in image.")
        else:
            st.error("City not found or API error.")
    except Exception as e:
        st.error(f"API request failed: {e}")
