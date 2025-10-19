# Multi-stage build for optimized CI/CD
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome (for Selenium)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

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
