# Dockerfile-frontend
FROM python:3.9

WORKDIR /app

RUN pip install streamlit requests

COPY . .

EXPOSE ${STREAMLIT_SERVER_PORT}

CMD ["streamlit", "run", "streamlit-ui-prompt-table.py"]