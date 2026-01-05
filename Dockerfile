# Base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY extractor.py .
COPY api ./api

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Render will map $PORT)
EXPOSE 10000

# Start FastAPI server
CMD ["uvicorn", "api.extract:app", "--host", "0.0.0.0", "--port", "10000"]
