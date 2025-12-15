# AI Workout Planner

A Streamlit app that uses a Hugging Face LLM to generate a 7-day workout plan with BMI context, safety notes, and nutrition tips.

## Features
- Collects height (cm), weight (kg), gender.
- Computes BMI and category, injects into the prompt.
- Uses a system prompt to enforce behavior as an expert fitness coach.
- Generates structured Markdown output: BMI summary, 7-day plan, safety/recovery, nutrition/hydration.
- Caches the Hugging Face pipeline to avoid reloading.

## Tech
- Python 3.10+
- Streamlit
- Hugging Face Inference API (default model: `mistralai/Mistral-7B-Instruct-v0.2`)

## Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate  # on Windows
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```

## Model notes
- Uses Hugging Face Inference API (no local GPU needed). Set env var `HF_TOKEN` or `HUGGINGFACEHUB_API_TOKEN` with your access token.
- Default model is set in `llm.py` via `DEFAULT_MODEL_NAME` (`mistralai/Mistral-7B-Instruct-v0.2`). Swap to another hosted model if desired. If you prefer `meta-llama/Meta-Llama-3-8B-Instruct`, set the name and ensure your token has access.
- Generation parameters are tuned for balanced creativity (`temperature=0.7`, `top_p=0.9`, `max_new_tokens=512`).

## Safety
- The app is informational only and does **not** provide medical advice.
- Displays disclaimer: "Consult a healthcare professional before starting any fitness program."

