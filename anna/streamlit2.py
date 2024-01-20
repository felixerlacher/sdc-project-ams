import streamlit as st
from transformers import pipeline


qa_pipeline = pipeline('question-answering', model='deepset/gelectra-large-germanquad', tokenizer='deepset/gelectra-large-germanquad', handle_impossible_answer=True)
def chatbot(question):
    # Provide context
    context = "Ich heiße Anna und bin der Berufsinfomat der AMS. Ich helfe dir gerne bei Fragen zu Ausbildungen und Berufen weiter."
    
    # Get the answer
    result = qa_pipeline(question=question, context=context)

    # Display the answer
    return result['answer']

st.title("AMS Berufsinfomat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hallo, wenn Sie Fragen zur Ausbildung oder Ihrer beruflichen weiteren Orientierung haben, dann sind Sie hier richtig! Fragen Sie den Berufsinfomat, und wir helfen Ihnen gerne weiter. Anonym und mit dem Wissen über 2.500 Berufe und Ausbildungen."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_response = chatbot(prompt)
    st.session_state.messages.append({"role": "assistant", "content": full_response})