import requests
from bs4 import BeautifulSoup
import re
import time
import logging
from config import BASE_URL

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_text_with_spans(p_tag):
    formatted_text = []
    for element in p_tag.contents:
        if element.name == 'span':
            span_text = element.get_text(strip=True)
            if span_text:
                formatted_text.append(f'"{span_text}"')
        else:
            normal_text = element.get_text(strip=True)
            if normal_text:
                formatted_text.append(normal_text)
    return ''.join(formatted_text)

def scrape_page(book_id, page_number, current_file_index, li_texts, retries=3):
    url = f"{BASE_URL}/{book_id}/{page_number}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                text_div = soup.find("div", class_="nass margin-top-10")
                
                if text_div:
                    paragraphs = text_div.find_all("p")
                    formatted_text = []
                    chunk_len = 0

                    for p in paragraphs:
                        text_with_spans = extract_text_with_spans(p)
                        text_with_spans = remove_tashkeel(text_with_spans)
                        
                        if text_with_spans == f'"{clean_text(li_texts[current_file_index])}"':
                            current_file_index += 1
                            chunk_len = len(formatted_text)
                            logger.info("Match found: %s vs %s", text_with_spans, f'"{clean_text(li_texts[current_file_index])}"')

                        formatted_text.append(text_with_spans)
                    
                    return formatted_text, current_file_index, chunk_len
                else:
                    logger.warning("Text div not found on page %d.", page_number)
                    return None, None, None
            elif response.status_code == 404:
                logger.warning("Page %d not found.", page_number)
                return None, None, None
        except requests.RequestException as e:
            logger.error("Attempt %d failed: %s", attempt + 1, e)
            time.sleep(2)
            
    logger.error("Failed to retrieve page %d after %d attempts.", page_number, retries)
    return None, None, None

def extract_li_text(soup):
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
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            li_texts = extract_li_text(soup)
                
            if li_texts:
                return li_texts
    except requests.RequestException as e:
        logger.error("Error fetching URL %s: %s", url, e)
    return []

def remove_tashkeel(text):
    return re.sub(r'[\u0617-\u061A\u064B-\u0652\[\]]', '', text).strip()

def clean_text(text):
    return re.sub(r'^-+', '', text).strip()
