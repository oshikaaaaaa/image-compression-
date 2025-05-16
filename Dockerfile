# Use official Python slim image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --timeout 30 || \
    pip install --no-cache-dir -r requirements.txt --timeout 60 || \
    pip install --no-cache-dir -r requirements.txt --timeout 120

# Copy app code
COPY ./app ./app

# Expose port your FastAPI app runs on
EXPOSE 8000

# Run the app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
