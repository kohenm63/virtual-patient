import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as gen_ai
import json  # For parsing hypothetical JSON feedback

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Please set the 'GOOGLE_API_KEY' environment variable.")
    st.stop()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

st.title("👨🏻‍⚕️ USMLE Medical Training Simulation - Step-by-Step Q&A")

# Start a new chat session if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat()

# Generate a scenario if not already present
if "scenario" not in st.session_state:
    scenario_prompt = "Generate a detailed USMLE-style medical scenario including vital signs, do not include Diagnosis, Lab Tests, Imaging"
    scenario_response = st.session_state.chat_session.send_message(scenario_prompt)
    st.session_state.scenario = scenario_response.text

st.header("Patient Scenario")
st.write(st.session_state.scenario)

# Questions and user input collection
questions = [
    "What is your initial diagnosis?",
    "What Imaging would you like to order?",
    "Describe your management plan for this patient.",
    "Any specific lab tests you want to order?"
]
responses = {question: st.text_input(question) for question in questions}

if st.button("Submit All Responses"):
    # Collect all responses into a single input for model evaluation
    structured_input = {
        "initial_diagnosis": responses["What is your initial diagnosis?"],
        "tests_ordered": responses["What tests would you like to order?"],
        "management_plan": responses["Describe your management plan for this patient."],
        "specific_lab_tests": responses["Any specific lab tests you want to order?"]
    }

    with st.spinner("Evaluating your responses..."):
        try:
            feedback_response = st.session_state.chat_session.send_message(input_to_model)
            feedback_data = feedback_response.text  # Assuming JSON output as an example
            feedback = json.loads(feedback_data) 

            st.subheader("Final Evaluation and Feedback")
            st.write("**Diagnosis:**")
            st.write(f"Correctness: {feedback['diagnosis']['correctness']}")
            st.write(f"Reasoning: {feedback['diagnosis']['reasoning']}")
            st.write("**Tests:**") 
            # ... Similarly display feedback on tests, management, etc.

        except Exception as e:  # Catch a general exception
            st.error("An error occurred. Please try again or contact the developers.")

if st.button("Start a New Case"):
    del st.session_state['scenario']
    del st.session_state['responses']
    st.experimental_rerun()
