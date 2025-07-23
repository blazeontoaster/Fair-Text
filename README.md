# Fair-Text: AI Bias Detector

## Overview
Detects bias in text (news, essays, feedback, etc.) and suggests fairer alternatives. Categories: race, gender, mental health, etc.

## Setup
1. Clone this repo
2. Install dependencies with Poetry:
   ```
   poetry install
   ```
3. Get an OpenAI API key and add it to a `.env` file:
   ```
   OPENAI_API_KEY=your-key-here
   ```
4. Run the app with Streamlit:
   ```
   poetry run streamlit run app.py
   ```

## Usage
- Open the local URL Streamlit provides (usually http://localhost:8501).
- Paste your text, click Analyze, and view flagged bias, suggestions, and categories.

## Extending
- Edit `prompt_templates.py` to add more categories or change prompt style.
- Build on the Streamlit UI or integrate with other tools as needed.