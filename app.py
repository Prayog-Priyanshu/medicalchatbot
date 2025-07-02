import streamlit as st
from openai import OpenAI

# Replace with your actual API key
OPENROUTER_API_KEY = "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"

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Page setup
st.set_page_config(page_title="Medical Chatbot", layout="centered")
st.title("🩺 Medical Chatbot")
st.markdown("Ask only medical-related questions!")

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your medical question:", "")
    submit = st.form_submit_button("Ask")

# Filter for medical keywords (very basic)
def is_medical_query(text):
    medical_keywords = [
        "symptom", "medicine", "fever", "treatment", "pain", "doctor", "infection", "disease", "pill",
        "dosage", "surgery", "virus", "bacteria", "injury", "health", "cancer", "tumor", "therapy",
        "diabetes", "blood", "x-ray", "scan", "headache", "allergy", "flu", "stroke", "organ", "heart", "covid"
    ]
    text = text.lower()
    return any(word in text for word in medical_keywords)


# Handle new user input
if submit and user_input:
    st.session_state.messages.append(("user", user_input))

    if is_medical_query(user_input):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                     model="nousresearch/deephermes-3-llama-3-8b-preview:free",
                    messages=[
                        {"role": "system", "content": "You are a helpful medical assistant. Only answer medical-related queries."},
                        {"role": "user", "content": user_input},
                    ],
                    extra_headers={
                        "HTTP-Referer": "https://yourdomain.com",  # Optional
                        "X-Title": "MedicalChatbot",                # Optional
                    },
                    extra_body={}
                )
                bot_reply = response.choices[0].message.content
                st.session_state.messages.append(("assistant", bot_reply))
            except Exception as e:
                st.session_state.messages.append(("assistant", f"❌ Error: {e}"))
    else:
        st.session_state.messages.append(("assistant", "⚠️ Please ask only medical-related questions."))

# Display chat history
for role, message in st.session_state.messages:
    if role == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
