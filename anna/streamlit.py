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

user_input = st.text_area("Hallo, wenn Sie Fragen zur Ausbildung oder Ihrer beruflichen weiteren Orientierung haben, dann sind Sie hier richtig! Fragen Sie den Berufsinfomat, und wir helfen Ihnen gerne weiter. Anonym und mit dem Wissen über 2.500 Berufe und Ausbildungen.")
if st.button("Send"):
    chatbot_response = chatbot(user_input)

    st.text(f"Chatbot: {chatbot_response}")
