import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv('/Users/tis/foam/github/PRH-API-Python-Client/external_repos/PrhScraper/.env')

# Get the username and password from environment variables
BRIGHT_DATA_USERNAME = os.getenv('BRIGHT_DATA_USERNAME')
BRIGHT_DATA_PASSWORD = os.getenv('BRIGHT_DATA_PASSWORD')

# Construct the proxy URL
proxy_url = f"http://{BRIGHT_DATA_USERNAME}-session-random:{BRIGHT_DATA_PASSWORD}@brd.superproxy.io:22225"
proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

# Test the proxy connection
try:
    response = requests.get("http://httpbin.org/ip", proxies=proxies)
    response.raise_for_status()
    print("Proxy connection successful:", response.json())
except requests.exceptions.RequestException as e:
    print("Proxy connection failed:", e)