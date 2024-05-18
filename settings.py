import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('/Users/tis/foam/github/PRH-API-Python-Client/external_repos/PrhScraper/.env')

# This affects only the PDF and HTML downloader.
# Scraping the IDs and parsing the files is single threaded.
THREADS = 1 #15

# The folder where the HTML and PDF files will be saved.
DATA_DIR = './DATA/'
OUTPUT_CSV_FILE = 'output.csv'
ID_FILE = 'ids.jsonl'

# Change the username and the password with your own.
# Let me know when you register a BrightData account and I will record a short video showing you how to set up a zone and whitelist your IP - it is not hard.
BRIGHT_DATA_USERNAME = os.getenv('BRIGHT_DATA_USERNAME')
BRIGHT_DATA_PASSWORD = os.getenv('BRIGHT_DATA_PASSWORD')

# DON'T CHANGE THIS
# The script will work with most proxy providers, but BrightData is probably the best in this case
<<<<<<< HEAD
ROTATING_PROXY = f'http://{BRIGHT_DATA_USERNAME}-session-random{{session}}:{BRIGHT_DATA_PASSWORD}@brd.superproxy.io22225'
=======
#ROTATING_PROXY = f'http://{BRIGHT_DATA_USERNAME}-session-random{{session}}:{BRIGHT_DATA_PASSWORD}@brd.superproxy.io:22225' #TODO
ROTATING_PROXY = f'http://{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}@brd.superproxy.io:22225'

>>>>>>> main
