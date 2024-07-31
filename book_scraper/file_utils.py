import os
import logging
from docx import Document
from fpdf import FPDF
from config import BOOKS_DIRECTORY


logger = logging.getLogger(__name__)


def create_book_directory(book_id):
    directory = os.path.join(BOOKS_DIRECTORY, str(book_id))
    os.makedirs(directory, exist_ok=True)
    return directory

def save_file(directory, filename, text, file_format='txt'):
    file_path = os.path.join(directory, filename)
    try:
        if file_format == 'txt':
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
        elif file_format == 'pdf':
            save_as_pdf(file_path, text)
        elif file_format == 'docx':
            save_as_docx(file_path, text)
        else:
            logger.error(f"Unsupported file format: {file_format}")
    except Exception as e:
        logger.error(f"Failed to save file {filename}: {e}")

def save_as_pdf(file_path, text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(file_path)
    logger.info(f"PDF saved: {file_path}")

def save_as_docx(file_path, text):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(file_path)
    logger.info(f"DOCX saved: {file_path}")
