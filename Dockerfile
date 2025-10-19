# Simple, reliable Dockerfile for CI/CD
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    # Add Chrome repository
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    # Install Chrome
    && apt-get install -y google-chrome-stable \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy framework code
COPY . .

# Create necessary directories
RUN mkdir -p logs reports screenshots

# Set environment variables for headless execution
ENV HEADLESS=true
ENV BROWSER=chrome
ENV PYTHONUNBUFFERED=1

# Default command runs pytest
CMD ["pytest", "-v", "--html=reports/test_report.html", "--self-contained-html"]

# Alternative commands (override with docker run):
# docker run automation-framework behave
# docker run automation-framework pytest -m smoke
# docker run automation-framework pytest tests/test_login.py
