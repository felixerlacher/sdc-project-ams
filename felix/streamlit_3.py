import streamlit as st
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, PromptPart

# Custom prompt part for the system message
class SystemPromptPart(PromptPart):
    def __init__(self, system_message):
        self.system_message = system_message

    def generate(self, data):
        return f"system\n{self.system_message}"

# Initialize LLM with the model path
chat = LlamaCpp(
    model_path="./LeoLM/leo-hessianai-7b-chat-ams-merged-16bit-q8_0.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
)

# Setup for conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# User input
query = st.text_input("Input your query", value="Was ist der beste Beruf?")
ask_button = st.button("Ask")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if query and ask_button:
    # Append the user query to the conversation history
    st.session_state.chat_history.append({"role": "user", "content": query})

    # Create the prompt template
    prompt = ChatPromptTemplate(
        messages=[
            SystemPromptPart("You are a helpful assistant."),
            *[
                PromptPart(content=message["content"], role=message["role"])
                for message in st.session_state.chat_history
            ],
        ]
    )

    # Invoke the conversation
    conversation = LLMChain(llm=chat, prompt=prompt, verbose=True, memory=memory)
    response = conversation.generate()
    response_content = response["choices"][0]["message"]["content"]
    
    # Append the response to the conversation history
    st.session_state.chat_history.append({"role": "assistant", "content": response_content})

    # Display the conversation history
    for message in st.session_state.chat_history:
        st.write(f"{message['role']}: {message['content']}")
