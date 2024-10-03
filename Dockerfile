FROM ubuntu:latest

# Environment variables
ENV PYTHONBUFFERED=1
ENV APP_HOME=/app
ENV PATH="/usr/lib/poppler:/usr/bin:${PATH}"

# Set working directory
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    python3 \
    python3-pip \
    && ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pdf2image pytesseract

# Expose application port
EXPOSE 8080

# Command to run the application
CMD ["python", "main.py"]
