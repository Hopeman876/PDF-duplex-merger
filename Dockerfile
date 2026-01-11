FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pdf_merger.py .

ENV PYTHONUNBUFFERED=1

CMD ["python3", "pdf_merger.py"] 

