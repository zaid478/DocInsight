"""
This module contains functions for scraping text from a website, processing the text. 
The text is extracted from specific HTML elements and cleaned of certain characters.
"""

import re
import time
import logging
from functools import wraps
import requests
from bs4 import BeautifulSoup
from config import BASE_URL

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retry(max_attempts=5, delay=2):
    """
    Decorator to retry a function call if a requests.RequestException is raised.

    Parameters:
        max_attempts (int): Maximum number of retry attempts (default is 5).
        delay (int): Delay between attempts in seconds (default is 2).

    Returns:
        function: A wrapper function that retries the decorated function on failure.

    Raises:
        requests.RequestException: Reraise the exception if all retry attempts fail.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    attempts += 1
                    logger.error("Attempt %d/%d failed: %s", attempts, max_attempts, e)
                    if attempts < max_attempts:
                        time.sleep(delay)
                    else:
                        logger.error("All %d attempts failed.", max_attempts)
                        raise
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2)
def scrape_page(book_id, page_number, current_file_index, li_texts):
    """
    Scrapes a specific page of a book and processes the text.

    Parameters:
        book_id (int): The ID of the book.
        page_number (int): The page number to scrape.
        current_file_index (int): The current file index for text chunking.
        li_texts (list): List of text items to match against.
        retries (int): Number of retry attempts for failed requests.

    Returns:
        tuple: Formatted text, updated file index, and chunk length.
    """
    url = f"{BASE_URL}/{book_id}/{page_number}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text_div = soup.find("div", class_="nass margin-top-10")

        if text_div:
            paragraphs = text_div.find_all("p")
            formatted_text = []
            chunk_len = 0

            for p in paragraphs:
                para = []
                for element in p.contents:
                    text = remove_tashkeel(element.get_text(strip=True))

                    if element.name == 'span':
                        if text:
                            if text == f'{clean_text(li_texts[current_file_index])}':
                                chunk_len = len(formatted_text)
                                logger.info("Match found: %s vs %s", text,
                                            f'"{clean_text(li_texts[current_file_index])}"')
                                current_file_index += 1

                            para.append(f'"{text}"')
                    else:
                        text = remove_tashkeel(element.get_text(strip=True))
                        if text:
                            para.append(text)
                formatted_text.append(" ".join(para))

            return formatted_text, current_file_index, chunk_len

        logger.warning("Text div not found on page %d.", page_number)
        return None, None, None

    logger.error("Failed to retrieve page %d .", page_number)
    return None, None, None

def extract_li_text(soup):
    """
    Extracts text from list items within the specified navigation div.

    Parameters:
        soup (BeautifulSoup): A BeautifulSoup object representing the HTML document.

    Returns:
        list: A list of text items extracted from the <li> tags.
    """
    s_nav_div = soup.find("div", class_="s-nav")
    if not s_nav_div:
        logger.warning("s-nav div not found.")
        return []

    li_texts = []
    s_nav_div_ul = s_nav_div.find("ul")
    for li in s_nav_div_ul:
        a_list = li.find_all('a')
        if len(a_list) == 1:
            li_texts.append(a_list[0].text.strip())
        else:
            li_texts.append(a_list[1].text.strip())
    logger.info("Extracted li texts: %s", li_texts)

    return li_texts

def get_li_text(url):
    """
    Retrieves and extracts list item texts from a given URL.

    Parameters:
        url (str): The URL to fetch and parse.

    Returns:
        list: A list of extracted text items from the <li> tags.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            li_texts = extract_li_text(soup)

            if li_texts:
                return li_texts
    except requests.RequestException as e:
        logger.error("Error fetching URL %s: %s", url, e)
    return []

def remove_tashkeel(text):
    """
    Removes diacritical marks (tashkeel) from Arabic text.

    Parameters:
        text (str): The text to clean.

    Returns:
        str: The cleaned text without tashkeel.
    """
    return re.sub(r'[\u0617-\u061A\u064B-\u0652\[\]]', '', text).strip()

def clean_text(text):
    """
    Cleans text by removing leading hyphens.

    Parameters:
        text (str): The text to clean.

    Returns:
        str: The cleaned text without leading hyphens.
    """
    return re.sub(r'^-+', '', text).strip()
