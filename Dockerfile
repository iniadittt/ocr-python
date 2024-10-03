# Use Debian as the base image
FROM debian:latest

# Environment variables
ENV PYTHONBUFFERED=1
ENV APP_HOME=/app
ENV VENV_PATH="$APP_HOME/venv"
ENV PATH="$VENV_PATH/bin:$PATH"

# Set working directory
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    poppler-utils \
    tesseract-ocr \
    && ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv $VENV_PATH

# Copy application code
COPY . .

# Install Python dependencies in the virtual environment
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pdf2image pytesseract \
    pip install --no-cache-dir -r requirements.txt &&

# Expose application port
EXPOSE 8080

# Command to run the application
CMD ["python", "main.py"]
