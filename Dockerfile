FROM python:3.11-slim
ENV PYTHONBUFFERED=1
ENV APP_HOME=/app
ENV PATH="/usr/lib/poppler:/usr/bin:${PATH}"
WORKDIR $APP_HOME
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pdf2image pytesseract
EXPOSE 8080
CMD ["python", "main.py"]