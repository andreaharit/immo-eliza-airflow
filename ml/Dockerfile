# app/Dockerfile

FROM python:3.9-slim

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app

COPY ./0-Resources /app/0-Resources
COPY ./4-Predict_deploy /app/4-Predict_deploy


WORKDIR /app/4-Predict_deploy

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "house_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]