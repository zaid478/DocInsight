import requests
from bs4 import BeautifulSoup
from scraper import scrape_page, get_li_text
from file_utils import save_file,create_book_directory
from config import BOOK_ID, FILE_FORMAT, MAX_PAGES
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_and_chunk_book(book_id, file_format='txt'):
    # Create directory for the book
    directory = create_book_directory(book_id)
    page_number = 1
    current_file_index = 1
    
    url = f"https://shamela.ws/book/{book_id}/{page_number}"

    li_texts = get_li_text(url)
    
    if not li_texts:
        logger.info("No li texts found.")
        return
    current_file_text = ""

    while True:
        try:
            logger.info(f"Page Number: {page_number}.")
 
            formatted_text, new_file_index, chunk_len = scrape_page(book_id, page_number, current_file_index, li_texts)
            if formatted_text is None:
                break

            if new_file_index != current_file_index:
                current_file_text += '\n'.join(formatted_text[:chunk_len]) + '\n'
                
                file_name = f"{li_texts[current_file_index-1]}.{file_format}"
                save_file(directory, file_name, current_file_text, file_format)
                
                current_file_index = new_file_index
                current_file_text = "\n".join(formatted_text[chunk_len:])
            else:
                current_file_text += '\n'.join(formatted_text) + '\n'

            if MAX_PAGES and page_number >= MAX_PAGES:
                logger.info(f"Reached maximum pages limit: {MAX_PAGES}.")
                break
            page_number += 1
                
        except requests.RequestException as e:
            logger.error(f"Error fetching page {page_number}: {e}")
            break
        
    if current_file_text:
        file_name = f"{li_texts[current_file_index-1]}.{file_format}"
        save_file(directory, file_name, current_file_text, file_format)

# Main entry point
if __name__ == "__main__":
    scrape_and_chunk_book(BOOK_ID, FILE_FORMAT)
