#!/usr/bin/env python3
import time
import os
from pathlib import Path
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter

SOURCE_DIR = os.getenv('SOURCE_DIRECTORY', '/input')
OUTPUT_DIR = os.getenv('DESTINATION_DIRECTORY', '/output')
DELETE_ORIGINALS = os.getenv('DELETE_OLD_FILES', 'True').lower() == 'true'
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '10'))

class PDFMerger:
    def __init__(self):
        print(f"PDF Duplex Merger watching {SOURCE_DIR}, output to {OUTPUT_DIR}")
        print(f"Delete originals: {DELETE_ORIGINALS}, Check interval: {CHECK_INTERVAL}s")
    
    def get_pdf_files(self):
        """Gibt die zwei aeltesten PDF-Dateien zurueck"""
        pdf_files = sorted(
            [f for f in Path(SOURCE_DIR).glob('*.pdf')],
            key=lambda x: x.stat().st_mtime
        )
        return pdf_files[:2] if len(pdf_files) >= 2 else []
    
    def merge_pdfs(self, pdf1, pdf2):
        """Merged zwei PDFs alternierend (pdf1 normal, pdf2 invertiert)"""
        try:
            reader1 = PdfReader(str(pdf1))
            reader2 = PdfReader(str(pdf2))
            writer = PdfWriter()
            
            # Rueckseiten invertieren
            pages2 = list(reversed(reader2.pages))
            
            # Alternierend zusammenfuehren
            max_pages = max(len(reader1.pages), len(pages2))
            for i in range(max_pages):
                if i < len(reader1.pages):
                    writer.add_page(reader1.pages[i])
                if i < len(pages2):
                    writer.add_page(pages2[i])
            
            # Output-Datei erstellen
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path(OUTPUT_DIR) / f'merged_{timestamp}.pdf'
            
            with open(output_file, 'wb') as out:
                writer.write(out)
            
            print(f"Merged {pdf1.name} + {pdf2.name} -> {output_file.name}")
            
            # Originale loeschen wenn gewuenscht
            if DELETE_ORIGINALS:
                pdf1.unlink()
                pdf2.unlink()
                print(f"Deleted originals")
            
            return True
            
        except Exception as e:
            print(f"Error merging PDFs: {e}")
            return False
    
    def run(self):
        """Hauptschleife"""
        while True:
            pdf_files = self.get_pdf_files()
            
            if len(pdf_files) == 2:
                print(f"Found 2 PDFs: {pdf_files[0].name}, {pdf_files[1].name}")
                time.sleep(2)
                self.merge_pdfs(pdf_files[0], pdf_files[1])
            
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    merger = PDFMerger()
    merger.run()