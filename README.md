# sdc-project-ams Berufsberatungsbot

## berfuslexikon_scrape.ipynb
This notebook scrapes the ~1400 profession from the website berufslexikon.at and saves it to a json

## just_finetuning_leo-hessianai-mistral.ipynb
This notebook creates a QLORA adapter for the pretrained model from huggingface.co/leo-hessianai-mistral on the scraped data from berufslexikon.at

## convert_hf_to_gguf.ipynb
rougly describes how to merge q convert the huggingface model to a gguf model servable with llama.cpp -> CPU instead of GPU

## streamlit-fastapi-app
This folder contains the streamlit app and the fastapi server. The streamlit app is used for the frontend and the fastapi server is used for the backend. The backend is used to serve the model and to handle the requests from the frontend.