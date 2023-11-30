FROM python:3.9-slim

WORKDIR /app

COPY REST_main.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "REST_main.py"]