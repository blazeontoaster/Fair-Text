# Fair-Text: AI Bias Detector

## Overview
Detects bias in text (news, essays, feedback, etc.) and suggests fairer alternatives. Categories: race, gender, mental health, etc.

## Setup
1. Clone this repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Get an OpenAI API key and add it to a `.env` file:
   ```
   OPENAI_API_KEY=your-key-here
   ```
4. Run the server:
   ```
   uvicorn main:app --reload
   ```

## Usage
POST to `/analyze` with JSON:
```
{
  "text": "She’s emotional and unstable."
}
```
Response:
```
{
  "flagged": ["She’s emotional", "unstable"],
  "suggestions": ["She raised concerns", "experiencing challenges"],
  "categories": ["gender", "mental health"]
}
```

## Extending
- Edit `prompt_templates.py` to add more categories or change prompt style.
- Build a web UI or integrate with Google Docs, email, etc.