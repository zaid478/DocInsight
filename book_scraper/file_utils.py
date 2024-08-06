"""
Utility functions for handling file operations related to book scraping and processing.

This module provides functions for creating directories, saving text in different formats
(txt, pdf, docx), and logging the operations.
"""

import os
import logging
from docx import Document
from fpdf import FPDF
from config import BOOKS_DIRECTORY

logger = logging.getLogger(__name__)

def create_book_directory(book_id):
    """
    Creates a directory for the given book ID if it doesn't exist.

    Parameters:
        book_id (int): The ID of the book.

    Returns:
        str: The path to the created or existing directory.
    """
    directory = os.path.join(BOOKS_DIRECTORY, str(book_id))
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info("Directory created: %s", directory)
    except OSError as e:
        logger.error("Failed to create directory %s: %s", directory, e)
        raise
    return directory

def save_file(directory, filename, text, file_format='txt'):
    """
    Saves text to a file in the specified format.

    Parameters:
        directory (str): The directory where the file will be saved.
        filename (str): The name of the file.
        text (str): The text content to save.
        file_format (str): The format to save the file in ('txt', 'pdf', or 'docx').

    Returns:
        None
    """
    file_path = os.path.join(directory, filename)
    try:
        if file_format == 'txt':
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            logger.info("TXT file saved: %s", file_path)
        elif file_format == 'pdf':
            save_as_pdf(file_path, text)
        elif file_format == 'docx':
            save_as_docx(file_path, text)
        else:
            logger.error("Unsupported file format: %s", file_format)
    except (OSError, IOError) as e:
        logger.error("Failed to save file %s: %s", filename, e)
        raise

def save_as_pdf(file_path, text):
    """
    Saves text as a PDF file.

    Parameters:
        file_path (str): The path to save the PDF file.
        text (str): The text content to save.

    Returns:
        None
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(file_path)
        logger.info("PDF saved: %s", file_path)
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Failed to save PDF %s: %s", file_path, e)
        raise

def save_as_docx(file_path, text):
    """
    Saves text as a DOCX file.

    Parameters:
        file_path (str): The path to save the DOCX file.
        text (str): The text content to save.

    Returns:
        None
    """
    try:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)
        logger.info("DOCX saved: %s", file_path)
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Failed to save DOCX %s: %s", file_path, e)
        raise
