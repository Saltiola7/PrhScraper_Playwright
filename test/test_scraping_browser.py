import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('/Users/tis/foam/github/PRH-API-Python-Client/external_repos/PrhScraper/.env')

# Get the username and password from environment variables
<<<<<<< HEAD:test/test_proxy_bright_data.py
BRIGHT_DATA_USERNAME = os.getenv('BRIGHT_DATA_SCRAPING_BROWSER_USERNAME')
BRIGHT_DATA_PASSWORD = os.getenv('BRIGHT_DATA_SCRAPING_BROWSER_PASSWORD')
=======
#BRIGHT_DATA_USERNAME = os.getenv('BRIGHT_DATA_USERNAME')
#BRIGHT_DATA_PASSWORD = os.getenv('BRIGHT_DATA_PASSWORD')

BRIGHT_DATA_USERNAME = 'brd-customer-hl_91c8167a-zone-scraping_browser_prh'
BRIGHT_DATA_PASSWORD = 'l9o4dlg9ie26'
>>>>>>> main:test/test_scraping_browser.py

# Construct the AUTH string
AUTH = f'{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}'
SBR_WS_CDP = f'wss://{AUTH}@brd.superproxy.io:9222'

# Ensure the output directory exists
output_dir = '/Users/tis/foam/github/PRH-API-Python-Client/external_repos/PrhScraper/test/out'
os.makedirs(output_dir, exist_ok=True)

async def run(pw):
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        print('Connected! Navigating...')
        page = await browser.new_page()
        await page.goto('https://virre.prh.fi', timeout=2*60*1000)
        print('Taking page screenshot to file page.png')
        await page.screenshot(path=os.path.join(output_dir, 'page.png'), full_page=True)
        print('Navigated! Scraping page content...')
        html = await page.content()
        print(html)
        
        # CAPTCHA solving: If you know you are likely to encounter a CAPTCHA on your target page, add the following few lines of code to get the status of Scraping Browser's automatic CAPTCHA solver
        # Note 1: If no captcha was found it will return not_detected status after detectTimeout
        # Note 2: Once a CAPTCHA is solved, if there is a form to submit, it will be submitted by default
        # client = await page.context.new_cdp_session(page)
        # solve_result = await client.send('Captcha.solve', { 'detectTimeout': 30*1000 })
        # status = solve_result['status']
        # print(f'Captcha solve status: {status}')
    finally:
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())