# streamlit_frontend.py
import streamlit as st
import requests


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




# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    response = requests.post("http://localhost:8000/chat/", json={"question": prompt})
    print(response.status_code)
    if response.status_code == 200:
        # Listen for the assistant's response
        response = requests.get("http://localhost:8000/stream", stream=True)
        print(response.status_code)
        if response.status_code == 200:
            with st.chat_message("assistant"):
                # Create a placeholder for the assistant's message
                message_placeholder = st.empty()
                for line in response.iter_lines():
                    # filter out keep-alive new lines
                    if line:
                        decoded_line = line.decode('utf-8')
                        # only do if find data  
                        if decoded_line.find('data:'):
                            # Extract the data after the 'data:' prefix
                            start_index = decoded_line.find('data:') + len('data:')
                            content = decoded_line[start_index:].strip()
                            #remove {''} from content
                            content = content[2:-2]
                            # Update the placeholder with the new message
                            message_placeholder.markdown(content)
                    #If the end of the message is reached, break the loop
                    if "<|im_end|>" in content:
                        break
                message = {"role": "assistant", "content": content}
                st.session_state.messages[-1] = message
            st.rerun()
        else:
            st.error("Error in processing the GET request")
    else:
        st.error("Error in processing the POST request")