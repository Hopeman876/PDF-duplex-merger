# PDF Duplex Merger

Automatische Zusammenführung von doppelseitig gescannten PDFs für Scanner ohne Duplexeinheit.

## Problem

Viele Scanner haben einen automatischen Dokumenteneinzug (ADF), aber keine Duplexeinheit. Bei doppelseitigen Dokumenten erhält man daher zwei separate PDF-Dateien:
- Eine PDF mit allen Vorderseiten (Seiten 1, 3, 5, 7, …)
- Eine PDF mit allen Rückseiten (Seiten 2, 4, 6, 8, …)

Diese müssen normalerweise manuell zusammengeführt werden, wobei die Rückseiten in umgekehrter Reihenfolge eingefügt werden müssen.

## Lösung

Dieser Docker-Container überwacht einen Ordner und führt automatisch zwei aufeinanderfolgende PDFs zusammen:
- Die erste PDF wird als Vorderseiten behandelt
- Die zweite PDF wird als Rückseiten behandelt (automatisch invertiert)
- Das Ergebnis wird mit Zeitstempel in einen Output-Ordner geschrieben
- Die Original-PDFs werden optional gelöscht (konfigurierbar)

## Features

- Keine speziellen Dateinamen nötig – funktioniert mit normalen Scannamen wie `Scan_001234.pdf`
- Automatische Erkennung über Zeitstempel (immer die zwei ältesten PDFs)
- Rückseiten werden automatisch in korrekter Reihenfolge invertiert
- Konfiguration über Umgebungsvariablen
- Mehrere Instanzen gleichzeitig möglich (z.B. für verschiedene Benutzer oder Scanner)
- Ideal als Vorstufe für synOCR oder andere DMS-/OCR-Lösungen
