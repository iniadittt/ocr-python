# Use the latest Ubuntu base image
FROM ubuntu:latest
ENV PYTHONBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
RUN apt-get update && \
    apt-get install -y python3 python3-pip poppler-utils tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*
COPY . ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install pdf2image pytesseract
EXPOSE 8080

# Command to run the application
CMD ["python3", "main.py"]
