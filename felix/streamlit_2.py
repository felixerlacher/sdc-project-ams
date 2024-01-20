from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import HumanMessage
import streamlit as st

from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.memory import ConversationBufferMemory

# Callbacks support token-wise streaming
#callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])




#class StreamHandler(BaseCallbackHandler):
class StreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, container, initial_text="", display_method='markdown'):
        self.container = container
        self.text = initial_text
        self.display_method = display_method

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        display_function = getattr(self.container, self.display_method, None)
        if display_function is not None:
            display_function(self.text)
        else:
            raise ValueError(f"Invalid display_method: {self.display_method}")
        


query = st.text_input("input your query", value="Was ist der beste Beruf?")
ask_button = st.button("ask")

st.markdown("### streaming box")
chat_box = st.empty()

#stream_handler = StreamHandler(chat_box, display_method='write')
#chat = ChatOpenAI(max_tokens=25, streaming=True, callbacks=[stream_handler])
callback_manager = CallbackManager([StreamHandler(chat_box, display_method='write')])

# Initialize LLM with the model path
chat = LlamaCpp(
    model_path="./LeoLM/leo-hessianai-7b-chat-ams-merged-16bit-q8_0.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,
    #chat_format="llama-2",
)

st.markdown("### together box")

# if query and ask_button:
#     response = chat([HumanMessage(content=query)])
#     llm_response = response.content
#     st.markdown(llm_response)


# Prompt setup
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "Du bist ein netter Berufsberatungsassistent."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# Conversation buffer memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=chat, prompt=prompt, verbose=True, memory=memory)

if query and ask_button:
    # Extract the content from the HumanMessage and pass it as a string
    response = conversation({"question": query})
    #llm_response = response.content
    st.markdown(response)