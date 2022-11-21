# Extend the official Rasa SDK image
FROM python:3.10-slim

# Use subdirectory as working directory
WORKDIR /app
COPY . .

RUN pip install -r requirements.txt


CMD ["python","./app.py"]
