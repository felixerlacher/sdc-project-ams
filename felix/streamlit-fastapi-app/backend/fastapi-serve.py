# fastapi_backend.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.llms import LlamaCpp
import uvicorn

import wandb
from langchain.callbacks import wandb_tracing_enabled
import os
wandb.login(key="247b3da94c9b88bd5e990f1d94799ca3ded57d6b")
run = wandb.init(project="fastapi-serve", job_type="interference")
os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
#os.environ["WANDB_PROJECT"] = "langchain-tracing"

app = FastAPI()

# Callbacks and LLM setup (similar to your initial setup)
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    #model_path="../../LeoLM/leo-mistral-hessianai-7b-ams-merged-16bit-q4_k_m.gguf",
    #model_path="../../LeoLM/leo-hessianai-7b-chat-ams-merged-16bit-q8_0.gguf",
    # for docker
    model_path="./leo-hessianai-7b-chat-ams-merged-16bit-q8_0.gguf",
    temperature=0.2,
    max_tokens=2000,
    context_window=2000,
    #context_window=2000,
    top_p=0.9,
    callback_manager=callback_manager,
    verbose=True,
    chat_format="Llama2"
)

# overwrite SystemMessagePromptTemplate to conform template:
# """
# <|im_start|>system
# {system_message}<|im_end|>
# <|im_start|>user
# {prompt}<|im_end|>
# <|im_start|>assistant
# """


prompt = ChatPromptTemplate(
    messages=[

        # SystemMessagePromptTemplate.from_template("\nDu bist assistent, du berätst human bei der Berufswahl. Du bist ausschließlich der ""assistant"", du wirst ausschließlich als dieser antworten, du wirst nicht als human antworten. Die bisherige Konversation ist hier nachzulesen: <|im_end|>\n<|im_start|>"),
        # MessagesPlaceholder(variable_name="chat_history"),
        # HumanMessagePromptTemplate.from_template("\n{question}<|im_end|>\n<|im_start|>assistant:\n"),
        SystemMessagePromptTemplate.from_template("\nDu befindest dich in einem Chat. Du bist der Assistant, und deine Aufgabe ist es, dem Human bei der Berufswahl zu beraten. Du agierst ausschließlich als 'Assistant' und antwortest nur in dieser Rolle. Du wirst unter keinen Umständen als 'Human' antworten. Die bisherige Konversation kann hier eingesehen werden: \n"),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("\n{question}\Assistant:\n"),

    ]
)

def log_conversation(prompt, response):
    wandb.log({"prompt": prompt, "response": response})

memory = ConversationBufferWindowMemory(k=3, memory_key="chat_history", return_messages=True)

conversation = LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)


class ChatRequest(BaseModel):
    question: str

@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    response = conversation({"question": chat_request.question})
    return {"response": response}

if __name__ == "__main__":

    uvicorn.run("fastapi-serve:app", host="0.0.0.0", port=80)