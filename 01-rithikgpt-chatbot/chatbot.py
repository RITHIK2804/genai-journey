import streamlit as st
from google import genai


st.set_page_config(
    page_title="RithikGPT",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RithikGPT")
st.caption("A ChatGPT-style chatbot built with Streamlit + Gemini")


# Gemini Client


client = genai.Client(api_key="")

# Session State

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat Inpu
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert chat history to Gemini format
    history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    # Get Gemini response
    response = client.models.generate_content(
        model="models/gemini-3.7-flash",
    
        contents=history
    )

    bot_reply = response.text

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })
