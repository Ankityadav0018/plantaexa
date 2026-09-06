FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create upload directory
RUN mkdir -p uploadimages

# Expose ports for Flask and Streamlit
EXPOSE 5000 8501

# Default: run Flask app
CMD ["python", "app.py"]
