FROM python:3.14-slim

# Sicherheitsupdates des Debian-Unterbaus einspielen, die seit dem
# letzten Release des Basis-Images erschienen sind
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# pip aktualisieren, Abhaengigkeiten installieren und nicht benoetigte
# Build-Tools (setuptools, wheel) entfernen
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y setuptools wheel

COPY pdf_merger.py .

ENV PYTHONUNBUFFERED=1

CMD ["python3", "pdf_merger.py"]
