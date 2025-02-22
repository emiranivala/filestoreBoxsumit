FROM python:3.10.4-slim-buster

# Update package lists and install required OS packages
RUN apt update && \
    apt-get install -y git curl ffmpeg wget bash

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Set working directory and copy your application code
WORKDIR /app
COPY . .

# Expose the port for your Flask application
EXPOSE 8000

# Start both the Flask app and the worker process concurrently.
CMD ["sh", "-c", "python app.py & python -m FileStoreBox"]
