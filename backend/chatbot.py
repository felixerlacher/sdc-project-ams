from huggingface_hub import InferenceClient
from transformers import pipeline
# Initialize client for a specific model
#client = InferenceClient(model="dbmdz/german-gpt2")
#client.conversational("Jemand da?")

pipe = pipeline('text-generation', model="dbmdz/german-gpt2",
                 tokenizer="dbmdz/german-gpt2")

text = pipe("Der Sinn des Lebens ist es", max_length=100)[0]["generated_text"]

print(text)