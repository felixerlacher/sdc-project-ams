import streamlit as st
import requests
import json

# Streamlit interface
st.title("Chat with FastAPI Backend")
system_prompt = st.text_area("Enter your system prompt:", value="", max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None)
message = st.text_area("Enter your user prompt:", value="", max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None)


if st.button("Send Message"):
    if message:
        # Construct the request payload
        payload = {
            "messages": [
                {"content": system_prompt, "role": "system"},
                {"content": message, "role": "user"}
            ]
        }

        # Endpoint of your FastAPI backend
        url = "http://localhost:8001/chatcompletions"

        # Make a POST request to the FastAPI backend
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            st.success("Message sent successfully!")
            st.write("Response:", response.json())
        else:
            st.error("Failed to send message. Status Code: " + str(response.status_code))
    else:
        st.error("Please enter a message.")
