import math
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()  # loads .env file
HF_TOKEN = os.getenv("HF_TOKEN")
from llm import generate_plan
from prompts import SYSTEM_PROMPT, build_user_prompt


def compute_bmi(height_cm: float, weight_kg: float) -> float:
    """Compute BMI using metric units."""
    height_m = height_cm / 100.0
    return weight_kg / (height_m**2)


def bmi_category(bmi: float) -> str:
    """Classify BMI into standard categories."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"


def build_prompt(
    height_cm: float,
    weight_kg: float,
    gender: str,
    goal: str,
    extra_instructions: str | None = None,
) -> str:
    """Combine system prompt and user prompt for the LLM."""
    bmi = compute_bmi(height_cm, weight_kg)
    category = bmi_category(bmi)
    user_prompt = build_user_prompt(
        height_cm,
        weight_kg,
        gender,
        bmi,
        category,
        goal,
        extra_instructions,
    )
    return f"{SYSTEM_PROMPT}\n\nUser:\n{user_prompt}\n\nAssistant:"


def main():
    # Load .env so HF_TOKEN is available when running locally.
    load_dotenv()
    st.set_page_config(page_title="AI Workout Planner", page_icon="💪", layout="centered")
    st.title("Workout Planner")
    

    with st.form("user_inputs"):
        col1, col2 = st.columns(2)
        with col1:
            height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
        with col2:
            weight_kg = st.number_input("Weight (kg)", min_value=25.0, max_value=250.0, value=70.0, step=0.5)

        gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
        goal = st.selectbox("Primary goal", options=["Muscle gain", "Fat loss", "General fitness"])
        custom_prompt = st.text_area(
            "Custom prompt (optional)",
            help="Add your own instructions, e.g. preferred equipment, schedule, or style of training.",
            height=100,
        )
        submitted = st.form_submit_button("Generate Workout Plan")

    if submitted:
        if height_cm <= 0 or weight_kg <= 0:
            st.error("Height and weight must be greater than zero.")
            return

        prompt = build_prompt(height_cm, weight_kg, gender, goal, custom_prompt)
        st.markdown("Your generated plan")
        with st.spinner("Generating plan..."):
            try:
                plan = generate_plan(prompt)
            except Exception as exc:  # pragma: no cover - defensive UX
                st.error(
                    "Generation failed. If the message mentions an API key or token, set environment "
                    "variable HF_TOKEN (or HUGGINGFACEHUB_API_TOKEN) with your Hugging Face access token. "
                    f"Details: {exc}"
                )
                return
        st.markdown(plan)




if __name__ == "__main__":
    main()

