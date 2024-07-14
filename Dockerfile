FROM python:3.12-slim

COPY . /app

COPY .cache /root/.cache/

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
    
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "st_app.py", "--server.port=8501", "--server.address=0.0.0.0"]