FROM python:3.11-slim

# Installation system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    sox \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setting the working directory
WORKDIR /app

# Installing Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Set the entry point
CMD ["python","-m", "app.main"]
