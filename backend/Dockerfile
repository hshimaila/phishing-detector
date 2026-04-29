FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

COPY . .

RUN mkdir -p saved_models ml_training/datasets

# Auto-train models during build if they don't exist
RUN python ml_training/download_datasets.py && \
    python ml_training/train_email_model.py && \
    python ml_training/train_url_model.py

EXPOSE 5000

CMD ["python", "run.py"]