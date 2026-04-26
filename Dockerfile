FROM python:3.10-slim

WORKDIR /app

COPY scanner/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scanner/ .

CMD ["python", "scanner.py"]
