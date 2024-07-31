
# Document Scraper Service

## Overview

The Document Scraper Service is a Python-based tool designed to scrape, process, and save text from online book pages. It extracts content from specified book URLs, processes it, and saves it in various formats (TXT, DOCX, PDF) based on user configuration. This service is useful for aggregating and analyzing large volumes of textual data from online sources.

## Features

- **Scrape Pages:** Extract content from web pages using BeautifulSoup.
- **Text Processing:** Handle and format text, including removing specific characters and cleaning up text.
- **Multiple Formats:** Save output in TXT, DOCX, or PDF formats.
- **Robust Error Handling:** Includes retry logic and detailed logging for better troubleshooting.

## Configuration

Configuration options are managed in the `config.py` file:

- **`BASE_URL`**: The base URL for scraping pages.
- **`BOOK_ID`**: The ID of the book to scrape.
- **`FILE_FORMAT`**: The format in which to save the files (txt, docx, pdf).
- **`MAX_PAGES`**: The maximum number of pages to scrape (set to `None` for no limit).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repository/document-scraper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd document-scraper
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Configure the settings**: Edit `config.py` to set `BOOK_ID`, `BASE_URL`, `FILE_FORMAT`, and `MAX_PAGES`.

2. **Run the scraper**: Execute the `main.py` script to start scraping.

    ```bash
    python main.py
    ```

