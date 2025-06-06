# Talent-scoutbot
Got it! Here’s a ready-to-use **README.md** file text for your Hiring Assistant Chatbot project that you can directly add to your repo:

````markdown
# Hiring Assistant Chatbot

## Project Overview

The **Hiring Assistant Chatbot** is an intelligent conversational assistant built for the fictional recruitment agency **TalentScout**. It automates the initial candidate screening by collecting personal and technical details, generating customized technical questions based on the candidate's skillset, and maintaining an engaging, interactive conversation powered by OpenAI's language models.

---

## Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/hiring-assistant-chatbot.git
   cd hiring-assistant-chatbot
````

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**

   Create a `.env` file in the project root with the following content:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the app:**

   ```bash
   streamlit run app.py
   ```

6. **Access the chatbot:**

   Open your web browser and go to `http://localhost:8501`

---

## Usage Guide

* On launch, the chatbot will greet the user and prompt for candidate details such as name, email, and technology skills.
* It dynamically generates technical questions tailored to the specified skills.
* The conversation flows naturally to simulate an interview experience.
* Recruiters can review candidate inputs at the end for quick pre-screening.

---

## Technical Details

* **Framework:** Streamlit for web UI.
* **LLM:** OpenAI GPT-3.5 (configurable for GPT-4 if available).
* **Language:** Python 3.9+
* **Main libraries:**

  * `openai`
  * `python-dotenv`
  * `streamlit`
* **Architecture:** Single `app.py` file managing UI, conversation logic, and API calls.
* **State Management:** Utilizes Streamlit’s session state to maintain dialogue context.

---

## Prompt Design

Prompts are designed to:

* Collect comprehensive candidate information.
* Use candidate skill inputs to generate relevant, clear technical questions.
* Maintain professional yet friendly dialogue tone.
* Keep conversations concise, adaptive, and user-friendly.

Example prompt snippet:

```
You are an interview assistant. First, ask the candidate's name and primary programming languages. Then generate 3 tailored technical questions based on those languages. End by thanking the candidate.
```

---

## Challenges & Solutions

* **Maintaining conversation context:** Used Streamlit session state for seamless multi-turn interaction.
* **Dynamic question generation:** Crafted flexible prompt templates integrating user skills.
* **API rate limiting:** Added error handling to notify users and suggest API plan upgrades.
* **Security:** Managed API keys securely via `.env` files and excluded them from source control.

---

Feel free to contribute or raise issues for improvements!

