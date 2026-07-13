FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (without spacy)
COPY requirements.txt .

# Install only essential packages
RUN pip install --no-cache-dir fastapi uvicorn python-multipart sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv scikit-learn pytesseract opencv-python Pillow numpy pandas joblib httpx beautifulsoup4 lxml pydantic-settings

# Copy application
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
