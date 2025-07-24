import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- Custom CSS for a modern, visually appealing dark UI ---
st.markdown('''
    <style>
    body {
        background: #181818 !important;
    }
    .main {
        background: #181818;
        border-radius: 16px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.07);
        padding: 32px 24px 24px 24px;
        max-width: 700px;
        margin: 40px auto;
    }
    .fade-out {
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.7s;
    }
    .result-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2.5rem;
        margin-top: 2.5rem;
        animation: fadeIn 1s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .result-box {
        background: #181818;
        border-radius: 14px;
        padding: 32px 28px;
        box-shadow: 0 2px 16px rgba(33,150,243,0.10);
        min-width: 350px;
        max-width: 700px;
        color: #fff;
        border: 2px solid #fff;
        margin-bottom: 0.5em;
    }
    .result-title {
        font-size: 2.1rem;
        color: #90caf9;
        font-weight: 700;
        margin-bottom: 0.7em;
        text-align: center;
        letter-spacing: 0.03em;
    }
    .result-text {
        font-size: 1.35rem;
        color: #e3f2fd;
        font-weight: 500;
        text-align: center;
        word-break: break-word;
    }
    .home-btn {
        display: block;
        margin: 2.5rem auto 0 auto;
        background: #1976d2;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 16px 36px;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
        box-shadow: 0 2px 8px rgba(33,150,243,0.10);
    }
    .home-btn:hover {
        background: #125ea7;
    }
    .stTextArea textarea {
        min-height: 120px;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        background: #181818;
        color: #fff;
        box-shadow: none;
    }
    .stTextArea textarea::placeholder {
        color: #b0b0b0;
        opacity: 1;
    }
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
    }
    h1, h4, label, .stRadio label, .stTextArea label, .footer {
        color: #fff !important;
    }
    .footer {
        text-align: center;
        color: #90a4ae !important;
        font-size: 0.95rem;
        margin-top: 40px;
    }
    </style>
''', unsafe_allow_html=True)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'original' not in st.session_state:
    st.session_state.original = ''
if 'paraphrased' not in st.session_state:
    st.session_state.paraphrased = ''
if 'bias_removed' not in st.session_state:
    st.session_state.bias_removed = ''

# --- Home/Input Page ---
if st.session_state.page == 'home':
    st.markdown("""
    <div class="main" id="main-card">
    <h1 style='text-align:center; background:#181818; color:#fff; border-radius:12px; padding:18px 0 18px 0; margin-bottom:0.5em;'>Fair-Text: AI Bias Detector</h1>
    <p style='text-align:center; color:#b0b0b0; font-size:1.15rem;'>Paste your text below. The app will flag potentially biased words or phrases and suggest more fair or neutral alternatives using Gemma 3 27B.</p>
    """, unsafe_allow_html=True)

    with st.form("analyze_form"):
        st.markdown("<h4 style='margin-bottom:0.5em;'>Input Text</h4>", unsafe_allow_html=True)
        text = st.text_area("", height=180, placeholder="Paste your text here...")
        st.markdown("<h4 style='margin-bottom:0.5em; margin-top:1.5em;'>Task</h4>", unsafe_allow_html=True)
        task = st.radio(
            "Choose task:",
            ("Paraphrase", "Bias Removal"),
            horizontal=True
        )
        submitted = st.form_submit_button("Analyze", use_container_width=True)

    if submitted:
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Generating all options with Gemma..."):
                try:
                    st.session_state.original = text
                    model = genai.GenerativeModel("models/gemma-3-27b-it")
                    # Paraphrased
                    para_prompt = f"Paraphrase the following text: {text}"
                    para_response = model.generate_content(para_prompt)
                    st.session_state.paraphrased = para_response.text if hasattr(para_response, 'text') else ''
                    # Bias Removed
                    bias_prompt = f"Rewrite the following sentence to remove any bias and avoid mentioning specific groups: {text}"
                    bias_response = model.generate_content(bias_prompt)
                    st.session_state.bias_removed = bias_response.text if hasattr(bias_response, 'text') else ''
                    st.session_state.page = 'results'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown("""
    <div class="footer">
      Fair-Text &copy; 2024 &mdash; Built with Streamlit, Google Gemini, and Gemma 3 27B
    </div>
    </div>
    """, unsafe_allow_html=True)

# --- Results Page ---
if st.session_state.page == 'results':
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    if st.button("Home", key="home-btn", help="Go back to input page", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown("""
    <div class="result-box">
        <div class="result-title">Original</div>
        <div class="result-text">{}</div>
    </div>
    <div class="result-box">
        <div class="result-title">Paraphrased</div>
        <div class="result-text">{}</div>
    </div>
    <div class="result-box">
        <div class="result-title">Bias Removed</div>
        <div class="result-text">{}</div>
    </div>
    </div>
    """.format(
        st.session_state.original,
        st.session_state.paraphrased,
        st.session_state.bias_removed
    ), unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
      Fair-Text &copy; 2024 &mdash; Built with Streamlit, Google Gemini, and Gemma 3 27B
    </div>
    """, unsafe_allow_html=True) 