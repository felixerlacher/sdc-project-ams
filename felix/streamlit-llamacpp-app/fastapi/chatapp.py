from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests
import json
from sse_starlette.sse import EventSourceResponse

# Define the Pydantic model for the incoming request
class IncomingRequest(BaseModel):
    messages: list[dict] = Field(..., example=[
        {"content": "You are a helpful assistant.", "role": "system"},
        {"content": "What is the capital of France?", "role": "user"}
    ])

# Define the Pydantic model for the outgoing response
class OutgoingResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[dict]
    usage: dict

app = FastAPI()


@app.post("/chatcompletions", response_model=OutgoingResponse)
async def send_request(data: IncomingRequest):
    url = "http://localhost:8000/v1/chat/completions"
    headers = {
        'accept': 'text/event-stream',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data.dict()))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error from the server")

    return response.json()

# To run the application, use the following command:
# uvicorn <this_file_name_without_py_extension>:app --reload