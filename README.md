# 🌐 Professional Indian Language Translator

A state-of-the-art translation and transliteration application built with Python and Streamlit. It bridges the gap between complex Indian languages and seamless digital communication using advanced voice and text technologies.

## ✨ Key Features

-   **🔤 Smart Translation**: Supports 13+ Indian languages (Telugu, Hindi, Tamil, etc.) with region-specific accuracy.
-   **🗣️ Live Voice Input**: Speak naturally directly into the app (Windows-optimized recording stack).
-   **✍️ Transliteration**: Type inside the app using English characters (e.g., *'namaste'*) and get native script (*'नमस्ते'*).
-   **🔊 Text-to-Speech**: Listen to translations with natural-sounding AI voices.
-   **🎨 Premium UI**: A modern, glassmorphic interface with animated backgrounds and intuitive UX.

## 🛠️ Technology Stack (Pin-to-Pin)

This project has been engineered for **Reliability** and **User Experience**.

| Component | Technology Used | Why? |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Rapid, pure-Python web interface development. |
| **Design** | CSS3 + Glassmorphism | To provide a premium, modern aesthetic over standard tools. |
| **Translation** | `deep-translator` | **Robust & Reliable**. Replaced flaky GoogleTrans for better uptime. |
| **Speech** | `sounddevice` + `scipy` | **Microphone Access**. Replaced PyAudio to fix Windows installation hell. |
| **Transliteration**| Google Input Tools API | Best-in-class conversion for Indian scripts. |

## 🚀 Installation & Setup

### Prerequisites
-   Python 3.8+
-   A working microphone

### Step 1: Clone & Install
```bash
# Clone repository
git clone <repository_url>
cd indian-language-translator

# Install dependencies (Updated for Stability)
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

## 📖 Documentation
-   **[Project Deep Dive (Pin-to-Pin Explanation)](project_deep_dive.md)**: A complete breakdown of *how* and *why* everything works. Read this to understand the code logic line-by-line.
-   **Implementation Plan**: See `implementation_plan.md` (Artifacts) for our development roadmap.

## 🐛 Troubleshooting

**1. "No Audio Detected" / Silent Recording**
-   Check your Windows Microphone Privacy settings.
-   Speak louder near the mic.
-   The app filters out silence (< 500 amplitude) automatically.

**2. "He is my friend" (Translation Errors)**
-   Some kinship terms (e.g., *Bammardi* in Telugu) are context-heavy. Current AI models may default to generic male terms. We use `deep-translator` to minimize this, but nuanced human relations are still a challenge for free AIs.

## 🎯 Supported Languages
Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Urdu, Kannada, Malayalam, Punjabi, Odia, Assamese, English.

---
*Built with ❤️ for Indian Languages.*
