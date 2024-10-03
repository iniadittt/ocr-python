# Use the latest Ubuntu base image
FROM ubuntu:latest
ENV PYTHONBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
RUN apt-get update && \
    apt-get install -y python python-pip poppler-utils tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*
COPY . ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pdf2image pytesseract
EXPOSE 8080

# Command to run the application
CMD ["python", "main.py"]
