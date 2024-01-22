# streamlit_frontend.py
import streamlit as st
import requests
import os

env_backend_url = os.environ['APP_BACKEND_URL']

st.header("Chat mit Berufsberater 💬 📚")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Frag mich zur Berufen!"}
    ]

if prompt := st.chat_input("Deine Frage"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

#print st.session_state.messages
# for i in range(len(st.session_state.messages)):
#     print(st.session_state.messages[i])


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Denke..."):
            response = requests.post(f"{env_backend_url}/chat/", json={"question": prompt})
            if response.status_code == 200:
                message = {"role": "assistant", "content": response.json().get("response")}
                st.session_state.messages.append({"role": "assistant", "content": message["content"]["text"]})
                st.rerun()
            else:
                st.error("Error in processing the request")

