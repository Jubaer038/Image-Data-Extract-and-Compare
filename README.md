

A **Streamlit-based mobile-friendly web app** to extract temperature from an image or photo and compare it with the current temperature from OpenWeather API.

---

## 🔹 Features

- Upload an image (JPG, JPEG, PNG)  
- Take a photo using device camera  
- Extract text from the image using OCR (`pytesseract`)  
- Detect valid temperature values (e.g., 28°C, 30 degree)  
- Compare extracted temperature with OpenWeather API  
- Show **Match / Not Match** in a card view  
- Scrollable history of previous comparisons  
- Mobile-friendly layout with responsive design  

---
## 🔹 Open in Browser / Mobile:
- Usually runs at `http://localhost:8501` 
---
## 🔹 Requirements

- Python 3.9+  
- Streamlit  
- Tesseract OCR installed locally  

### Python packages:

```bash
pip install streamlit pillow opencv-python-headless pytesseract requests numpy
```

### Tesseract Installation


```bash
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev
```

---

## 🔹 Project Structure

```
ImageDataExtractCompare/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🔹 Setup Instructions (Local Testing)

1. Clone the repository:
```bash
git clone <repository_link>
cd ImageDataExtractCompare
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Verify Tesseract installation:
```bash
tesseract --version
```

5. Run the Streamlit app:
```bash
streamlit run app.py
``` 


## 🔹 How to Use

1. **Select Input Tab:**  
   - 📤 **Upload Image:** Choose a local image file  
   - 📸 **Take Photo:** Capture an image using the device camera  

2. **OCR Extraction:**  
   - Uploaded / captured image → OCR automatically extracts text  
   - Only valid integer temperature values are considered  

3. **Compare with API:**  
   - Enter city name (default: Dhaka)  
   - Click **Compare with API**  
   - Displays extracted vs API temperature in **card view**  
   - Shows **Match / Not Match**  

4. **History Tracking:**  
   - Previous comparisons appear below in scrollable cards  
   - Each card displays: Extracted Temp, API Temp, City, Status  

---

## 🔹 Code Summary

- **Session State Variables:**
```python
st.session_state.image_file       # Uploaded or Camera image
st.session_state.extracted_temp    # OCR detected temperature
st.session_state.extracted_text    # Extracted OCR text
st.session_state.current_source    # 'upload' or 'camera'
st.session_state.history           # Previous comparisons
```

- **Tabs:** Upload / Camera input (`st.tabs`)  
- **OCR:** `pytesseract` + OpenCV grayscale conversion  
- **Temperature Extraction:** Regex `r'(\d+)\s*(?:°|°C|degree|degrees)'`  
- **API Compare:** OpenWeather API fetch + rounding  
- **Card View:** `st.columns` + `st.metric`  
- **History:** Scrollable display using session state  

---

## 🔹 Notes

- Internet connection required for OpenWeather API  
- Only integer temperatures extracted (no fractional like 28.5)  
- Multiple image inputs supported; previous results reset for new input  
- Mobile-friendly layout tested on phones and tablets  
