# fastapi_backend.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import LlamaCpp

from fastapi import FastAPI, Request
from typing import Generator
import sys
import asyncio

from typing import TYPE_CHECKING, Any, Dict, List

from langchain_core.outputs import LLMResult
if TYPE_CHECKING:
    from langchain_core.agents import AgentAction, AgentFinish
    from langchain_core.messages import BaseMessage
    from langchain_core.outputs import LLMResult

from sse_starlette.sse import EventSourceResponse

app = FastAPI()

streamed_data = []
llm_running = False

llm_result = None

#class StreamHandler(BaseCallbackHandler):
class StreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, container, initial_text="", display_method='markdown'):
        self.container = streamed_data
        self.text = initial_text
        self.llm_running = llm_running
        self.llm_result = llm_result


    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any ) -> None:
        """Run when LLM starts running."""
        self.llm_running = True

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.llm_result = response
        self.llm_running = False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        # Append the new token to the global list
        self.container.append(self.text)
        # sys.stdout.write(token)
        # sys.stdout.flush()
        
stream_handler = StreamHandler(streamed_data, display_method='write')
callback_manager = CallbackManager([stream_handler])

llm = LlamaCpp(
    model_path="../../LeoLM/leo-hessianai-7b-chat-ams-merged-16bit-q8_0.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,
    chat_format="llama-2",
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

        SystemMessagePromptTemplate.from_template("\nDu bist assistent, du berätst Human bei der Berufswahl.Du bist ausschließlich der ""assistant"", du wirst ausschließlich als dieser antworten. Beende deine antwort mit:""<|im_end|>"" <|im_end|>\n<|im_start|>"),
        #MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("\n{question}<|im_end|>\n<|im_start|>assistant:\n"),
    ]
)



memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=llm, prompt=prompt, verbose=False)#, memory=memory)

class ChatRequest(BaseModel):
    question: str

@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    response = conversation({"question": chat_request.question})
    print("message received")
    return {"response": response}


# @app.get("/stream", response_class=Response, media_type="text/event-stream")
# async def stream_data() -> Generator[str, None, None]:
#     while True:
#         if streamed_data:
#             data = streamed_data.pop(0)
#             yield f"data: {data}\n\n"

# @app.get("/stream")
# async def stream_data() -> Response:
#     async def event_stream() -> Generator[str, None, None]:
#         while True:
#             if streamed_data:
#                 data = streamed_data.pop(0)
#                 yield f"data: {data}\n\n"
#     return Response(event_stream(), media_type="text/event-stream")


STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

@app.get('/stream')
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        # check if callback_manager writes to streamed_data with llm_running
        return bool(streamed_data)
        
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                yield {
                        "data": streamed_data.pop(0),
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())