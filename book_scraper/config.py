"""
Configuration settings for the book scraping and processing application.

This module provides various configuration settings, such as directory paths,
book ID, base URL, file formats, and page settings. It also includes utility
functions for generating book directories and file paths.
"""

import os

# Directory settings
BOOKS_DIRECTORY = 'books'
BOOK_ID = 8183

BASE_URL = "https://shamela.ws/book"

# Format settings
FILE_FORMAT = 'docx'  # Options: 'txt', 'docx', 'pdf'
SUPPORTED_FORMATS = ['txt', 'docx']

# Page and retry settings
MAX_PAGES = None
RETRIES = 3

def get_book_directory(book_id):
    """
    Generates the directory path for the given book ID.

    Parameters:
        book_id (int): The ID of the book.

    Returns:
        str: The directory path for the book.
    """
    return os.path.join(BOOKS_DIRECTORY, str(book_id))

def get_file_path(book_id, filename):
    """
    Generates the file path for a given book ID and filename.

    Parameters:
        book_id (int): The ID of the book.
        filename (str): The name of the file.

    Returns:
        str: The full file path.
    """
    return os.path.join(get_book_directory(book_id), filename)
