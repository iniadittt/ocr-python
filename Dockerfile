FROM python:3.12-slim
RUN apt-get update && apt-get install -y poppler-utils
ENV PYTHONBUFFERED=1
ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "main.py"]