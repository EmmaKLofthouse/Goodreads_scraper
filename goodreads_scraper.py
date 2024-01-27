import concurrent.futures
import requests
from bs4 import BeautifulSoup
import json
from retrying import retry
import numpy as np
import sys

# Retry decorator with exponential backoff
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def make_request(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def scrape_book(bookID):
    page_url = f"https://www.goodreads.com/book/show/{bookID}"

    #if bookID % 100 == 0:
    #    print(f"Scraping book {bookID}")

    try:
        response = make_request(page_url)
    except requests.exceptions.RequestException as e:
        print(f"Error making request for book {bookID}: {e}")
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract JSON-LD data
        json_ld_script = soup.find('script', {'type': 'application/ld+json'})
        json_ld_content = json_ld_script.string if json_ld_script else None

        # Parse JSON data
        if json_ld_content:
            book_info = json.loads(json_ld_content)

            # Extract specific information
            title = book_info.get('name', 'N/A')
            number_of_pages = book_info.get('numberOfPages', 'N/A')
            language = book_info.get('inLanguage', 'N/A')
            author_name = book_info.get('author', [{}])[0].get('name', 'N/A')
            rating_value = book_info.get('aggregateRating', {}).get('ratingValue', 'N/A')
            rating_count = book_info.get('aggregateRating', {}).get('ratingCount', 'N/A')
            review_count = book_info.get('aggregateRating', {}).get('reviewCount', 'N/A')
            isbn = book_info.get('isbn', 'N/A')

            # Extract publication date from the webpage
            publication_date = extract_publication_date(soup)


            # Store the extracted data in a dictionary
            extracted_data = {
                'Title': title,
                'Number of Pages': number_of_pages,
                'Language': language,
                'Author': author_name,
                'Rating Value': rating_value,
                'Rating Count': rating_count,
                'Review Count': review_count,
                'ISBN': isbn,
                'Publication Date': publication_date
            }

            return extracted_data
    return None

def extract_publication_date(soup):
    publication_date_element = soup.find('p', {'data-testid': 'publicationInfo'})
    if publication_date_element:
        return publication_date_element.get_text(strip=True)
    else:
        return 'N/A'

def scrape_goodreads(start, end):
    extracted_data_list = []  # List to store extracted data for all books

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Scraping books concurrently using ThreadPoolExecutor
        results = list(executor.map(scrape_book, range(start, end)))

    # Filter out None results
    extracted_data_list.extend(filter(None, results))

    # Save the extracted data to a JSON file
    with open(f'extracted_data_{start}_to_{end-1}.json', 'w',
              encoding='utf-8') as json_file:
        json.dump(extracted_data_list, json_file, indent=2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 goodreads_scraper.py <start> <end>")
        sys.exit(1)

    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    except ValueError:
        print("Error: Start and end must be integers")
        sys.exit(1)

    # If a value is given for the number of books per file, use this
    # Otherwise, write out a file for every tenth of the range.
    # This is to avoid losing all the books if something goes wrong towards
    # the end of the scraping process.
    try:
        n_write_files = int(sys.argv[3])
        book_ranges = np.arange(start, end, n_write_files)
    except:
        book_ranges = [start,end]

    for start, end in zip(book_ranges[:-1], book_ranges[1:]):
        scrape_goodreads(start, end)