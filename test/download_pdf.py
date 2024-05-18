import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv('/path/to/your/.env')

BRIGHT_DATA_USERNAME = os.getenv('BRIGHT_DATA_USERNAME')
BRIGHT_DATA_PASSWORD = os.getenv('BRIGHT_DATA_PASSWORD')

PDF_URL = 'https://virre.prh.fi/novus/reportdisplay'
SEARCH_URL = 'https://virre.prh.fi/novus/companySearch'
COMPANY_ID = '0217665-9'  # Example company ID
OUTPUT_DIR = './output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_proxy_auth_header():
    proxy_auth = f"{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}"
    proxy_auth_encoded = base64.b64encode(proxy_auth.encode()).decode()
    return {"Proxy-Authorization": f"Basic {proxy_auth_encoded}"}

def load_bs_object_from_response(response):
    RATE_LIMIT_ERROR = 'Huomaa, että tänä aikana voi kuitenkin käyttää prh.fi-sivuja normaalisti.'
    if RATE_LIMIT_ERROR in response.text:
        raise Exception("Rate limit error")
    return BeautifulSoup(response.text, 'html.parser')

def parse_csrf_and_execution(bs_object):
    csrf_token = bs_object.select_one('input[name="_csrf"]').get('value')
    execution = bs_object.select_one('input[name="execution"]').get('value')
    return csrf_token, execution

def download_pdf():
    session = requests.Session()
    session.proxies = {
        "http": f"http://{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}@brd.superproxy.io:22225",
        "https": f"http://{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}@brd.superproxy.io:22225"
    }
    session.headers.update(get_proxy_auth_header())

    # Initial request to get CSRF token and execution ID
    init_response = session.get(SEARCH_URL)
    bs_object = load_bs_object_from_response(init_response)
    csrf_token, execution = parse_csrf_and_execution(bs_object)

    # Post search data
    search_post_data = {
        'execution': execution,
        'registrationNumber': '',
        'nameStateCode': '',
        'name': '',
        'companyStateCode': '',
        '_companyFormCode': '1',
        '_domicileCode': '1',
        'businessId': COMPANY_ID,
        '_csrf': csrf_token,
        '_eventId_search': 'Hae',
        '_exactNameMatch': 'on',
    }
    search_response = session.post(SEARCH_URL, data=search_post_data)
    bs_object = load_bs_object_from_response(search_response)

    # Extract company URL
    company_tag = bs_object.select_one('a[href*="companyId="]')
    if company_tag is None:
        raise Exception("Company not found")

    company_url = urljoin(SEARCH_URL, company_tag.get('href'))
    company_response = session.get(company_url)
    bs_object = load_bs_object_from_response(company_response)
    csrf_token, execution = parse_csrf_and_execution(bs_object)

    # Post data to create PDF
    pdf_post_data = {
        'execution': execution,
        '_csrf': csrf_token,
        '_eventId_createElectronicTRExtract': ''
    }
    session.post(SEARCH_URL, data=pdf_post_data)
    company_pdf_data = session.get(PDF_URL).content

    if company_pdf_data[0:5].decode('utf-8') != '%PDF-':
        raise Exception('Invalid PDF.')

    # Save the PDF
    pdf_path = os.path.join(OUTPUT_DIR, f"{COMPANY_ID}.pdf")
    with open(pdf_path, 'wb') as f:
        f.write(company_pdf_data)
    print(f"PDF downloaded successfully to {pdf_path}")

if __name__ == "__main__":
    download_pdf()