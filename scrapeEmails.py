import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import time

def extract_emails_from_text(text):
    return re.findall(r'[\w\.-]+@[\w\.-]+', text)

def scrape_website_for_emails(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()

        emails = extract_emails_from_text(text_content)
        return emails
    except requests.exceptions.HTTPError as e:
        print(f"Error accessing {url}: HTTP Error {e.response.status_code}")
    except Exception as e:
        print(f"Error accessing {url}: {e}")
    return []

def google_search_company_emails(company_name):
    query = f"{company_name} email"
    search_results = list(search(query, num_results=1, lang='en'))

    if search_results:
        print(f"Search results for {company_name}: {search_results[0]}")
        return scrape_website_for_emails(search_results[0])
    else:
        print(f"No search results found for {company_name}")
        return []

def get_company_emails_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            company_names = file.read().splitlines()

        company_emails_mapping = {}
        for company_name in company_names:
            emails = google_search_company_emails(company_name)
            company_emails_mapping[company_name] = emails
            # delay of 2 seconds between requests
            time.sleep(2)

        return company_emails_mapping
    except Exception as e:
        print(f"Error while processing the file: {e}")
        return {}

if __name__ == "__main__":
    file_path = "namen.txt"
    company_emails = get_company_emails_from_file(file_path)

    print("Company emails extracted:")
    for company_name, emails in company_emails.items():
        print(f"{emails}")