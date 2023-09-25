FROM python:3.9-slim

WORKDIR /app

COPY ./analytics.py .
COPY ./requirements.txt .
COPY ./app.py .
COPY ./dashboard_utils.py .
COPY ./minio_utils.py .
COPY ./images/ .

# Set an environment variable
ENV MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
ENV MINIO_SECRET_KEY=${MINIO_SECRET_KEY}
ENV MINIO_SECRET_KEY=${FLASK_BASE_URL}

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]