# Dockerfile-backend
FROM python:3.9

WORKDIR /app

RUN pip install fastapi pydantic langchain wandb wheel llama-cpp-python uvicorn

# Copy the .gguf file into the container
COPY ./leo-hessianai-7b-chat-ams-merged-16bit-q8_0.gguf /app

# Copy fastapi-serve.py into the container
COPY ./fastapi-serve.py /app

EXPOSE 80

CMD ["python3", "fastapi-serve.py"]
#CMD ["python3", "-m", "llama_cpp.server", "--host", "0.0.0.0", "--port", "8000", "--model", "leo-mistral-hessianai-7b-chat-ams-merged-q8_0.gguf"]