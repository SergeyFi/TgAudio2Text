FROM python:3.11-slim

# Installation system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setting the working directory
WORKDIR /workspace

# Installing Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a user for VSCode
RUN useradd -m vscode
USER vscode
