import uuid

import requests
import streamlit as st

# Paste your n8n production webhook URL here
WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL"

st.title("🤝 Your Personal Assistant")
st.subheader("What can your personal assistant do?")
st.markdown("""
1. Answer questions on various topics.
2. Arrange Calendar events and meetings.
3. Read your emails and send replies, can even summarize them for you.
4. Manage your tasks and to-do lists.
5. Take quick notes for you.
6. Track your expenses and budgeting.
""")

st.subheader("💬 Chat with your assistant")

# Session state: chat history and a unique session id for memory
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Type your message...")

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    # Send the message to the n8n webhook
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={"message": user_message, "session_id": st.session_state.session_id},
            timeout=120,
        )
        data = response.json()
        ai_response = data.get("output") or f"n8n error ({response.status_code}): {data}"
    except Exception as e:
        ai_response = f"Could not reach the assistant: {e}"

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)