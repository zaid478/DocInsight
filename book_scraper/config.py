# config.py

import os

# Directory settings
BOOKS_DIRECTORY = 'books'
BOOK_ID = 8183

BASE_URL = "https://shamela.ws/book"

# Format settings
FILE_FORMAT = 'txt'  # Options: 'txt', 'docx', 'pdf'
SUPPORTED_FORMATS = ['txt', 'docx']

# TODO ADD PDF SUPPORT 

# Page and retry settings
MAX_PAGES = None
RETRIES = 3

def get_book_directory(book_id):
    return os.path.join(BOOKS_DIRECTORY, str(book_id))

def get_file_path(book_id, filename):
    return os.path.join(get_book_directory(book_id), filename)
