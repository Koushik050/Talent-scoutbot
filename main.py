import streamlit as st
import re
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()

# --- LLM Service Class ---
class LLMService:
    def __init__(self):
        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            if not self.client.api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set or invalid.")
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {e}.")
            st.stop()

    def get_chat_completion(self, messages, temperature=0.7, model="gpt-3.5-turbo"):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred while getting LLM response: {e}"

    def generate_technical_questions(self, tech_stack):
        prompt = f"""You are TalentScout's AI Hiring Assistant. Generate 3 to 5 interview questions per tech.
        Tech stack: {tech_stack}.
        Output format:
        Python:
        1. ...
        """

        messages = [
            {"role": "system", "content": "You are a technical recruiter generating interview questions."},
            {"role": "user", "content": prompt}
        ]

        return self.get_chat_completion(messages, temperature=0.5)

# --- Candidate Data Manager ---
class CandidateDataManager:
    def __init__(self, filename="candidate_data.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                st.warning("Corrupted or empty JSON. Starting fresh.")
        return {}

    def _save_data(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            st.error(f"Error saving data: {e}")

    def add_candidate_info(self, email, info):
        if not email:
            st.warning("Email is required to save data.")
            return
        self.data[email] = info
        self._save_data()
        st.success(f"Data for {email} saved successfully.")

# --- Initialize Services ---
llm_service = LLMService()
data_manager = CandidateDataManager()

# --- Streamlit UI Setup ---
st.set_page_config(page_title="TalentScout AI", page_icon="🤖")
st.title("🤖 TalentScout AI Hiring Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.candidate_info = {
        "Full Name": None,
        "Email Address": None,
        "Phone Number": None,
        "Years of Experience": None,
        "Desired Position(s)": None,
        "Current Location": None,
        "Tech Stack": None
    }
    st.session_state.current_phase = "greeting"
    st.session_state.tech_stack_parsed = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm TalentScout's AI Assistant. Let's begin. What's your **Full Name**?"})

# --- Display Chat ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Logic ---
if user_input := st.chat_input("Type your response here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    candidate_info = st.session_state.candidate_info
    current_phase = st.session_state.current_phase
    assistant_response = ""

    if current_phase == "greeting":
        candidate_info["Full Name"] = user_input.strip()
        st.session_state.current_phase = "email"
        assistant_response = f"Nice to meet you, {candidate_info['Full Name']}! What's your **Email Address**?"

    elif current_phase == "email":
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", user_input):
            candidate_info["Email Address"] = user_input.strip()
            st.session_state.current_phase = "phone"
            assistant_response = "Great. What's your **Phone Number**?"
        else:
            assistant_response = "Invalid email. Please try again."

    elif current_phase == "phone":
        if re.match(r"^\+?[\d\s-]{7,20}$", user_input):
            candidate_info["Phone Number"] = user_input.strip()
            st.session_state.current_phase = "yoe"
            assistant_response = "How many **Years of Experience** do you have?"
        else:
            assistant_response = "Invalid phone number. Try again."

    elif current_phase == "yoe":
        try:
            yoe = int(user_input)
            if yoe >= 0:
                candidate_info["Years of Experience"] = yoe
                st.session_state.current_phase = "position"
                assistant_response = "What **Position(s)** are you applying for?"
            else:
                assistant_response = "Experience can't be negative."
        except ValueError:
            assistant_response = "Enter a number please."

    elif current_phase == "position":
        candidate_info["Desired Position(s)"] = user_input.strip()
        st.session_state.current_phase = "location"
        assistant_response = "What's your **Current Location** (City, Country)?"

    elif current_phase == "location":
        candidate_info["Current Location"] = user_input.strip()
        st.session_state.current_phase = "tech_stack"
        assistant_response = "List your **Tech Stack** separated by commas (e.g., Python, React, SQL)."

    elif current_phase == "tech_stack":
        parsed = [t.strip() for t in user_input.split(',') if t.strip()]
        if parsed:
            candidate_info["Tech Stack"] = user_input
            st.session_state.tech_stack_parsed = parsed
            st.session_state.current_phase = "generate_questions"
            assistant_response = f"Thanks! Generating questions for: **{', '.join(parsed)}**."
        else:
            assistant_response = "Please provide a valid tech stack."

    elif current_phase == "generate_questions":
        tech_stack_str = ", ".join(st.session_state.tech_stack_parsed)
        with st.spinner("Generating questions..."):
            questions = llm_service.generate_technical_questions(tech_stack_str)
        assistant_response = f"Here are your questions:\n\n{questions}\n\nType 'done' to finish."
        st.session_state.current_phase = "final_notes"

    elif current_phase == "final_notes":
        if user_input.lower() == "done":
            st.session_state.current_phase = "ended"
            final_message = "Thank you! We'll review your info and get back to you soon."
            st.session_state.messages.append({"role": "assistant", "content": final_message})
            data_manager.add_candidate_info(candidate_info["Email Address"], candidate_info)
            with st.chat_message("assistant"):
                st.markdown(final_message)
        else:
            assistant_response = "If you're done, type 'done' to complete."

    if assistant_response:
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
