import httpx
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('/Users/tis/foam/github/PRH-API-Python-Client/external_repos/PrhScraper/.env')

BRIGHT_DATA_USERNAME = os.getenv('BRIGHT_DATA_USERNAME')
BRIGHT_DATA_PASSWORD = os.getenv('BRIGHT_DATA_PASSWORD')

def test_proxy_connection():
    proxy_url = f'http://{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}@brd.superproxy.io:22225'
    print(f"Testing proxy: {proxy_url}")
    try:
        response = httpx.get("http://lumtest.com/myip.json", proxies={"http://": proxy_url, "https://": proxy_url})
        print(response.json())
    except Exception as e:
        print(f"Proxy test failed: {e}")

# Call the test function
test_proxy_connection()