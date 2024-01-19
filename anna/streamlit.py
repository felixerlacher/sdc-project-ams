import streamlit as st

st.title("AMS Berufsinfomat")

user_input = st.text_area("Hallo, wenn Sie Fragen zur Ausbildung oder Ihrer beruflichen weiteren Orientierung haben, dann sind Sie hier richtig! Fragen Sie den Berufsinfomat, und wir helfen Ihnen gerne weiter. Anonym und mit dem Wissen über 2.500 Berufe und Ausbildungen.")
if st.button("Send"):
    chatbot_response = chatbot_function(user_input)

    st.text(f"Chatbot: {chatbot_response}")
