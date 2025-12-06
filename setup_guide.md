# 🛠️ Setup Guide: Indian Language Translator

This guide provides step-by-step instructions to set up the **Indian Language Translator** on your local machine.

> **🎉 GOOD NEWS**: We have removed the reliance on `PyAudio`, which was causing major installation issues on Windows. The project now uses `sounddevice`, which installs easily!

## 📋 Prerequisites
-   **Python 3.8** or higher installed.
-   **pip** (Python package installer).
-   **Git** (optional, for cloning).

---

## 🚀 Installation Steps

### 1. Create a Virtual Environment (Recommended)
It is best practice to run this project in an isolated environment.

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Project Dependencies
We use `sounddevice` for audio and `deep-translator` for translation logic.

```bash
pip install -r requirements.txt
```

**What gets installed?**
-   `streamlit`: The web framework.
-   `deep-translator`: Google Translation engine (Robust).
-   `sounddevice`: Pure Python audio recording.
-   `scipy`: WAV file writing.
-   `numpy`: Fast array processing.
-   `SpeechRecognition`: Speech-to-text processing.
-   `gTTS`: Text-to-speech engine.

### 3. Run the Application
Start the Streamlit server:

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8502`.

---

## 🧪 Verifying Installation

1.  **Check Microphone**: Go to the "Speech Translation" tab and click "Start Speaking". If you see "Listening...", `sounddevice` is working.
2.  **Check Translation**: Go to "Text Translation", type "Hello" in English and translate to Hindi. If you see "नमस्ते", `deep-translator` is working.

## ⚠️ Common Issues

**Error: "Microphone not found"**
-   Ensure your browser (or terminal if running locally) has permission to access the microphone.
-   On Windows: Settings > Privacy > Microphone > Allow desktop apps to access your microphone.

**Error: "Translation Error"**
-   Check your internet connection. `deep-translator` requires an active connection to Google's servers.

---
*Setup Complete! Enjoy your translator.*
