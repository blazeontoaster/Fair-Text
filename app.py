import streamlit as st
import openai
import os
from dotenv import load_dotenv
from prompt_templates import BIAS_DETECTOR_PROMPT
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Fair-Text: AI Bias Detector", page_icon="📝", layout="centered")
st.title("Fair-Text: AI Bias Detector")
st.markdown("""
Paste your text below. The AI will flag potentially biased words or phrases and suggest more fair or neutral alternatives. Categories include race, gender, and mental health.
""")

with st.form("analyze_form"):
    text = st.text_area("Text to analyze", height=180)
    submitted = st.form_submit_button("Analyze")

if submitted:
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing for bias..."):
            try:
                prompt = BIAS_DETECTOR_PROMPT.format(text=text)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that detects bias in text."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=512,
                    temperature=0.2
                )
                result = response["choices"][0]["message"]["content"]
                data = json.loads(result)
                st.success("Analysis complete!")
                st.markdown("**Flagged Phrases:**")
                st.write(data.get("flagged", []))
                st.markdown("**Suggestions:**")
                st.write(data.get("suggestions", []))
                st.markdown("**Categories:**")
                st.write(data.get("categories", []))
            except Exception as e:
                st.error(f"Error: {e}") 