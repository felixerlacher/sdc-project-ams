FROM python:3.9

#
WORKDIR /app

#
#COPY ../backend/requirements.txt /app/requirements.txt

#
#RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install llama-cpp-python[server]

#
#COPY . /

EXPOSE 8000

# Copy the .gguf file into the container
COPY ../LeoLM/leo-mistral-hessianai-7b-chat-ams-merged-q8_0.gguf /app

# Run the server when the container launches
#CMD ["python3 -m llama_cpp.server --model app/leo-mistral-hessianai-7b-ams-merged-16bit-q4_k_m.gguf"]
#CMD ["python3", "-m", "llama_cpp.server", "--model", "leo-mistral-hessianai-7b-ams-merged-16bit-q4_k_m.gguf"]
CMD ["python3", "-m", "llama_cpp.server", "--host", "0.0.0.0", "--port", "8000", "--model", "leo-mistral-hessianai-7b-chat-ams-merged-q8_0.gguf"]