import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from textblob import TextBlob
import os
import base64
from io import BytesIO
import tempfile
import time
import requests
import json

import numpy as np
import uuid
from deep_translator import GoogleTranslator

# Page configuration
st.set_page_config(
    page_title="Indian Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Professional CSS with New Color Palette
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - solid black */
    .stApp {
        background: #010400;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean card design */
    .clean-card {
        background: #30332E;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #62BBC1;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: #62BBC1;
        font-size: 3rem;
        font-weight: 700;
        margin: 2rem 0 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .sub-header {
        text-align: center;
        color: #FFFBFC;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Button styling */
    .stButton>button {
        background: #62BBC1;
        color: #010400;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #30332E;
        color: #62BBC1;
        transform: translateY(-1px);
    }
    
    /* Text areas */
    .stTextArea textarea {
        background: #010400;
        border: 2px solid #30332E;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1rem;
        color: #FFFBFC;
    }
    
    .stTextArea textarea:focus {
        border: 2px solid #62BBC1;
        outline: none;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: #010400;
        border: 2px solid #30332E;
        border-radius: 8px;
        color: #FFFBFC;
    }
    
    .stSelectbox > div > div:hover {
        border: 2px solid #62BBC1;
    }
    
    /* File uploader */
    .stFileUploader {
        background: #30332E;
        border: 2px dashed #62BBC1;
        border-radius: 8px;
        padding: 1.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #30332E;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #FFFBFC;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #62BBC1;
        color: #010400;
    }
    
    .stTabs [aria-selected="true"] {
        background: #62BBC1;
        color: #010400;
    }
    
    /* Sentiment badges */
    .sentiment-badge {
        display: inline-block;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    
    .positive {
        background: #62BBC1;
        color: #010400;
    }
    
    .negative {
        background: #30332E;
        color: #FFFBFC;
        border: 2px solid #62BBC1;
    }
    
    .neutral {
        background: #30332E;
        color: #FFFBFC;
        border: 2px solid #62BBC1;
    }
    
    /* Stats card */
    .stats-card {
        background: #30332E;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #62BBC1;
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        color: #96705B;
    }
    
    .stats-label {
        color: #FFFBFC;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo, .stWarning {
        background: #30332E;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #62BBC1;
        color: #FFFBFC;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #30332E;
        border-right: 1px solid #62BBC1;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #62BBC1;
        font-weight: 700;
        font-size: 1.2rem;
        margin-top: 1.5rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFBFC;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #62BBC1;
    }
    
    [data-testid="stMetricLabel"] {
        color: #FFFBFC;
        font-weight: 600;
        opacity: 0.8;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #30332E;
        border-radius: 8px;
        padding: 1rem;
        font-weight: 600;
        color: #FFFBFC;
        border: 1px solid #62BBC1;
    }
    
    .streamlit-expanderHeader:hover {
        background: #684756;
        color: white;
    }
    
    /* Translation output */
    .translation-output {
        background: #30332E;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #62BBC1;
        color: #FFFBFC;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Audio player */
    audio {
        width: 100%;
        margin: 1rem 0;
    }
    
    /* Section headers */
    h3 {
        color: #96705B;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Paragraph text */
    p {
        color: #FFFBFC;
        opacity: 0.9;
    }
    
    /* Labels */
    label {
        color: #FFFBFC !important;
        font-weight: 500 !important;
    }
    
    /* Divider */
    hr {
        border-color: #62BBC1;
        opacity: 0.3;
    }
</style>
""", unsafe_allow_html=True)

# Supported Indian languages
INDIAN_LANGUAGES = {
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Gujarati': 'gu',
    'Urdu': 'ur',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Punjabi': 'pa',
    'Odia': 'or',
    'Assamese': 'as',
    'English': 'en'
}

# Speech Recognition Locales
INDIAN_LANG_SPEECH_CODES = {
    'hi': 'hi-IN',
    'bn': 'bn-IN',
    'te': 'te-IN',
    'mr': 'mr-IN',
    'ta': 'ta-IN',
    'gu': 'gu-IN',
    'ur': 'ur-IN',
    'kn': 'kn-IN',
    'ml': 'ml-IN',
    'pa': 'pa-IN',
    'or': 'or-IN',
    'as': 'as-IN',
    'en': 'en-IN'
}

# Input Tools Codes for Transliteration
INDIAN_LANG_INPUT_CODES = {
    'hi': 'hi-t-i0-und',
    'bn': 'bn-t-i0-und',
    'te': 'te-t-i0-und',
    'mr': 'mr-t-i0-und',
    'ta': 'ta-t-i0-und',
    'gu': 'gu-t-i0-und',
    'ur': 'ur-t-i0-und',
    'kn': 'kn-t-i0-und',
    'ml': 'ml-t-i0-und',
    'pa': 'pa-t-i0-und',
    'or': 'or-t-i0-und',
    'as': 'as-t-i0-und'
}

# Initialize session state
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'total_translations' not in st.session_state:
    st.session_state.total_translations = 0

# Initialize session state

def transliterate_text(text, lang_code):
    """Transliterate text using Google Input Tools API"""
    if lang_code not in INDIAN_LANG_INPUT_CODES or not text:
        return None
    
    try:
        input_code = INDIAN_LANG_INPUT_CODES[lang_code]
        url = "https://inputtools.google.com/request"
        params = {
            'text': text,
            'itc': input_code,
            'num': '1',
            'cp': '0',
            'cs': '1',
            'ie': 'utf-8',
            'oe': 'utf-8'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            res_json = response.json()
            if res_json[0] == 'SUCCESS' and res_json[1]:
                # res_json[1][0][1] contains the list of suggestions
                return res_json[1][0][1][0]
    except Exception as e:
        st.error(f"Transliteration Error: {e}")
        return None
    return None



def translate_text(text, source_lang, target_lang):
    """Translate text from source to target language"""
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None

def text_to_speech(text, lang):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")
        return None

def speech_to_text(audio_file):
    """Convert speech to text"""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        st.error(f"Speech recognition error: {str(e)}")
        return None

def analyze_sentiment(text):
    """Analyze sentiment of text"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = "Positive"
            emoji = "😊"
            css_class = "positive"
        elif polarity < -0.1:
            sentiment = "Negative"
            emoji = "😔"
            css_class = "negative"
        else:
            sentiment = "Neutral"
            emoji = "😐"
            css_class = "neutral"
        
        return sentiment, polarity, emoji, css_class
    except Exception as e:
        st.error(f"Sentiment analysis error: {str(e)}")
        return None, None, None, None

def get_audio_player(audio_bytes):
    """Create HTML audio player"""
    audio_base64 = base64.b64encode(audio_bytes.read()).decode()
    audio_html = f"""
    <audio controls style="width: 100%;">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """
    return audio_html

# Header
st.markdown('<h1 class="main-header">🌐 Indian Language Translator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional Multilingual Communication Platform</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Features")
    st.markdown("""
    - 🔤 Text Translation
    - 🎤 Speech Recognition
    - 🔊 Text-to-Speech
    - 💭 Sentiment Analysis
    - 📊 Real-time Processing
    - 📝 Translation History
    """)
    
    st.markdown("---")
    st.markdown("### 📈 Statistics")
    st.metric("Total Translations", st.session_state.total_translations)
    st.metric("Supported Languages", len(INDIAN_LANGUAGES))
    
    st.markdown("---")
    st.markdown("### ℹ️ Technology")
    st.markdown("""
    - Python & Streamlit
    - Google Translate API
    - NLP (TextBlob)
    - Speech Recognition
    - gTTS Engine
    """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📝 Text Translation", "🎤 Speech Translation", "💭 Sentiment Analysis", "📜 History"])

with tab1:
    st.markdown("### Text Translation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang_name = st.selectbox("Source Language", list(INDIAN_LANGUAGES.keys()), key="text_source")
        source_lang = INDIAN_LANGUAGES[source_lang_name]
        
        # Transliteration Toggle
        if source_lang != 'en':
            enable_transliteration = st.checkbox("✍️ Enable Transliteration (Type in English)", value=True, help="Type in English characters (e.g., 'namaste') and it will be converted to the native script.")
        else:
            enable_transliteration = False
        
    with col2:
        target_lang_name = st.selectbox("Target Language", list(INDIAN_LANGUAGES.keys()), index=1, key="text_target")
        target_lang = INDIAN_LANGUAGES[target_lang_name]
    
    input_text = st.text_area("Enter text to translate:", height=150, placeholder="Type your text here...")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        translate_btn = st.button("🔄 Translate", use_container_width=True)
    
    with col2:
        speak_source_btn = st.button("🔊 Play Source", use_container_width=True)
    
    with col3:
        speak_target_btn = st.button("🔊 Play Translation", use_container_width=True)
    
    if translate_btn and input_text:
        with st.spinner("Processing..."):
            final_input_text = input_text
            transliterated_text = None
            
            # 1. Handle Transliteration
            if enable_transliteration and source_lang != 'en':
                transliterated = transliterate_text(input_text, source_lang)
                if transliterated:
                    final_input_text = transliterated
                    transliterated_text = transliterated
                    st.info(f"**Interpreted Input ({source_lang_name}):** {transliterated}")
            
            # 2. Translation Logic
            translated_result = None
            
            # Case A: Self-Translation (Source == Target) -> Just return the transliterated text
            if source_lang == target_lang and enable_transliteration:
                translated_result = final_input_text
                st.success("✅ Transliteration completed!")
            
            # Case B: Standard Translation
            else:
                translated_result = translate_text(final_input_text, source_lang, target_lang)
                if translated_result:
                    st.success("✅ Translation completed!")

            if translated_result:
                st.markdown("### Translated Text:")
                st.markdown(f'<div class="translation-output">{translated_result}</div>', unsafe_allow_html=True)
                
                # Check for "same text" issue
                if translated_result.lower().strip() == final_input_text.lower().strip() and source_lang != target_lang:
                     st.warning("⚠️ The translation looks identical to the input. If you typed in English but meant a different language, make sure 'Enable Transliteration' is checked.")
                
                # Save to history
                history_original = f"{input_text}\n({transliterated_text})" if transliterated_text else input_text
                
                st.session_state.translation_history.append({
                    'source': source_lang_name,
                    'target': target_lang_name,
                    'original': history_original,
                    'translated': translated_result,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
                st.session_state.total_translations += 1
                
                # Store in session for audio playback
                st.session_state.current_source_text = final_input_text # Speak the Native Script if available
                st.session_state.current_source_lang = source_lang
                st.session_state.current_translated_text = translated_result
                st.session_state.current_target_lang = target_lang
    
    if speak_source_btn and input_text:
        with st.spinner("Generating audio..."):
            audio_fp = text_to_speech(input_text, source_lang)
            if audio_fp:
                st.markdown("### Source Audio:")
                st.markdown(get_audio_player(audio_fp), unsafe_allow_html=True)
    
    if speak_target_btn and hasattr(st.session_state, 'current_translated_text'):
        with st.spinner("Generating audio..."):
            audio_fp = text_to_speech(st.session_state.current_translated_text, st.session_state.current_target_lang)
            if audio_fp:
                st.markdown("### Translation Audio:")
                st.markdown(get_audio_player(audio_fp), unsafe_allow_html=True)
    

with tab2:
    st.markdown("### Speech Translation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        speech_source_lang_name = st.selectbox("Audio Language", list(INDIAN_LANGUAGES.keys()), key="speech_source")
        speech_source_lang = INDIAN_LANGUAGES[speech_source_lang_name]
    
    with col2:
        speech_target_lang_name = st.selectbox("Translate To", list(INDIAN_LANGUAGES.keys()), index=1, key="speech_target")
        speech_target_lang = INDIAN_LANGUAGES[speech_target_lang_name]
    
    audio_file = st.file_uploader("Upload Audio File (WAV format)", type=['wav'])

    st.markdown("---")
    if audio_file is not None:
        st.markdown("### 🎧 Audio Player")
        st.audio(audio_file)
        
        if st.button("🏁 Start Processing"):
            # Progress bar for visual feedback
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # 1. Speech to Text
                status_text.text("🎤 Converting Speech to Text...")
                progress_bar.progress(25)
                
                # Use speech_recognition
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio_data = recognizer.record(source)
                    # Use English as default fallback or map from selection
                    language_code = 'en-IN'
                    # Simple mapping - could be improved with INDIAN_LANG_SPEECH_CODES
                    # But for now let's rely on basic recognizer or user selection if we had mapped it correctly
                    # Looking at keys: 'hi', 'bn' etc.
                    if speech_source_lang_name in ['Hindi', 'Bengali', 'Tamil', 'Telugu', 'Marathi', 'Gujarati', 'Urdu', 'Kannada', 'Malayalam', 'Punjabi', 'Odia']:
                         # Very rough mapping attempt if dictionary keys match
                         pass
                    
                    # Better: use the dictionary defined at top
                    # We need to find the key for speech_source_lang_name
                    # INDIAN_LANGUAGES values are codes like 'hi', 'bn'
                    # INDIAN_LANG_SPEECH_CODES maps 'hi' -> 'hi-IN'
                    
                    lang_code_short = INDIAN_LANGUAGES.get(speech_source_lang_name, 'en')
                    lang_code_full = INDIAN_LANG_SPEECH_CODES.get(lang_code_short, 'en-IN')
                    
                    recognized_text = recognizer.recognize_google(audio_data, language=lang_code_full)
                
                if recognized_text:
                    progress_bar.progress(50)
                    st.success("✅ Speech Recognized!")
                    st.markdown(f"**Original ({speech_source_lang_name}):**")
                    st.markdown(f'<div class="translation-output">{recognized_text}</div>', unsafe_allow_html=True)
                    
                    # 2. Translation
                    status_text.text("🔄 Translating...")
                    progress_bar.progress(75)
                    
                    translated_text = translate_text(recognized_text, speech_source_lang, speech_target_lang)
                    
                    if translated_text:
                        progress_bar.progress(100)
                        status_text.text("✨ Completed!")
                        st.markdown(f"**Translation ({speech_target_lang_name}):**")
                        st.markdown(f'<div class="translation-output">{translated_text}</div>', unsafe_allow_html=True)
                        
                        # Save to history
                        st.session_state.translation_history.append({
                            'source': speech_source_lang_name,
                            'target': speech_target_lang_name,
                            'original': recognized_text,
                            'translated': translated_text,
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'Live Speech'
                        })
                        st.session_state.total_translations += 1
                        
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio. Please ensure clear speech.")
            except sr.RequestError as e:
                st.error(f"❌ Could not request results; {e}")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

with tab3:
    st.markdown("### Sentiment Analysis")
    
    sentiment_text = st.text_area("Enter text for sentiment analysis:", height=150, key="sentiment_input")
    
    if st.button("🔍 Analyze Sentiment"):
        if sentiment_text:
            with st.spinner("Analyzing..."):
                sentiment, polarity, emoji, css_class = analyze_sentiment(sentiment_text)
                
                if sentiment:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f'''
                        <div class="stats-card">
                            <div class="stats-number">{emoji}</div>
                            <div class="stats-label">Emotion</div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                    with col2:
                        st.markdown(f'''
                        <div class="stats-card">
                            <div class="stats-number">{sentiment}</div>
                            <div class="stats-label">Sentiment</div>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with col3:
                         st.markdown(f'''
                        <div class="stats-card">
                            <div class="stats-number">{polarity:.2f}</div>
                            <div class="stats-label">Polarity</div>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="sentiment-badge {css_class}">{emoji} {sentiment} Sentiment</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### Understanding Results:")
                    st.markdown(f"""
                    **Polarity Score:** {polarity:.3f} (ranges from -1.0 to +1.0)
                    
                    **Scale:**
                    - Positive: +0.1 to +1.0
                    - Neutral: -0.1 to +0.1
                    - Negative: -1.0 to -0.1
                    """)
        else:
            st.warning("⚠️ Please enter text to analyze.")
    

with tab4:
    st.markdown("### Translation History")
    
    if st.session_state.translation_history:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Total Records:** {len(st.session_state.translation_history)}")
        with col2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.translation_history = []
                st.rerun()
        
        st.markdown("---")
        
        for idx, item in enumerate(reversed(st.session_state.translation_history), 1):
            type_badge = f"🎤 {item.get('type', 'Text')}" if 'type' in item else "📝 Text"
            with st.expander(f"{type_badge} • {item['timestamp']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Source ({item['source']}):**")
                    st.markdown(f'<div class="translation-output">{item["original"]}</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown(f"**Target ({item['target']}):**")
                    st.markdown(f'<div class="translation-output">{item["translated"]}</div>', unsafe_allow_html=True)
    else:
        st.info("📭 No translation history yet. Start translating to see your history here!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #62BBC1; padding: 2rem; opacity: 0.9;'>
    <p style='font-size: 1rem; font-weight: 600;'>🌐 Indian Language Translator</p>
    <p style='font-size: 0.85rem; color: #FFFBFC;'>Powered by Google Translate • gTTS • NLP</p>
</div>
""", unsafe_allow_html=True)
