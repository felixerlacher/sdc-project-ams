# fastapi_backend.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.llms import LlamaCpp
import uvicorn

import wandb
from langchain.callbacks import wandb_tracing_enabled
import os
wandb.login(key="247b3da94c9b88bd5e990f1d94799ca3ded57d6b")
run = wandb.init(project="fastapi-serve", job_type="interference")
os.environ["LANGCHAIN_WANDB_TRACING"] = "true"

app = FastAPI()

# activate callbacks for streaming stdout or look override the callback manager for more options
# Callbacks and LLM setup (similar to your initial setup)
#callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    #model_path="./LeoLM/leo-hessianai-7b-chat-ams-merged-16bit-q8_0.gguf",
    #model_path="./leo-mistral-hessianai-7b-chat-ams-merged-q8_0.gguf",
    #model_path="./LeoLM/leo-mistral-hessianai-7b-ams-merged-16bit-q5_k_m.gguf",
    #model_path="./LeoLM/leo-mistral-hessianai-7b-ams-merged-16bit-f16.gguf",
    model_path="./leo-hessianai-7b-chat-ams-merged-q8_0.gguf",
    temperature=0.5,
    n_ctx = 1024,
    max_tokens=2000,
    top_p=0.95,
    #callback_manager=callback_manager,
    #verbose=True,  # Verbose is required to pass to the callback manager
    model_kwargs={"chat_format": "llama-2"},
    # also remove "<dummy00007>", i think there was a problem with the tokenizer, "<|im_end|>" -> "<dummy00007>, <|im_start|> -> "dummy00006>"
    stop = ["<|im_end|>", "<|im_start|>", "<dummy00007>"],
    echo=True,
    seed = 42
)


prompt_template = PromptTemplate.from_template("""
<|im_start|>system
Du befindest dich in einem Chat. Du bist der Assistant, und deine Aufgabe ist es, bei der Berufswahl zu beraten. Du agierst ausschließlich als 'Assistant' und antwortest nur in dieser Rolle. Die bisherige Konversation kann hier eingesehen werden:\n{chat_history}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
""")

prompt = "Hallo, ich würde beruflich gerne etwas in Richtung Machine Learning machen. Was würdest du mir empfehlen?"

memory = ConversationBufferWindowMemory( k=3, return_messages=True)  # Set the desired window size

class ChatRequest(BaseModel):
    question: str

async def llm_call(question):
    memory.load_memory_variables({})  # Load memory variables
    prompt = prompt_template.format(prompt=question, chat_history=memory.chat_memory.messages)
    print("\n\n\nPrompt: ", prompt, "\n\n\n")
    response = llm.generate([prompt])
    content = response.generations[0][0].text
    print("\n\n\nContent: ", content, "\n\n\n")
    memory.save_context({"user": question}, {"assistant": content})  # Save assistant output to memory
    #print("\n\n\nMemory: ", memory, "\n\n\n")
    return content

# endpoint
@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    print(chat_request)
    response = await llm_call(chat_request.question)
    return {"response": response}

if __name__ == "__main__":

    uvicorn.run("fastapi-serve-prompt-table:app", host="0.0.0.0", port=80)