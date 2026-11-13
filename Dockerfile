FROM python:3.15-slim

# Sicherheitsupdates des Debian-Unterbaus einspielen, die seit dem
# letzten Release des Basis-Images erschienen sind
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Abhaengigkeiten installieren und danach pip selbst entfernen: Zur Laufzeit
# wird es nicht gebraucht, und es bringt eine eigene, veraltete
# setuptools-Kopie mit (CVE-2025-47273)
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip setuptools wheel

COPY pdf_merger.py .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Nicht als root laufen. Die ID laesst sich in der Compose-Datei ueber
# "user:" an den Besitzer der eingebundenen Ordner anpassen.
USER 1000:1000

CMD ["python3", "pdf_merger.py"]
