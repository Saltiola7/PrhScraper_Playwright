import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
import requests
from pw_browser import launch_browser, close_browser
from pw_navigation import navigate_to_page, search_company, wait_for_download_button
from pw_download import download_pdf, get_cookies

# Load environment variables from .env file
load_dotenv('/Users/tis/foam/github/PRH-API-Python-Client/external_repos/PrhScraper/.env')

# Get the username and password from environment variables
#BRIGHT_DATA_USERNAME = os.getenv('BRIGHT_DATA_USERNAME')
#BRIGHT_DATA_PASSWORD = os.getenv('BRIGHT_DATA_PASSWORD')

BRIGHT_DATA_USERNAME = 'brd-customer-hl_91c8167a-zone-scraping_browser_prh'
BRIGHT_DATA_PASSWORD = 'l9o4dlg9ie26'

# Construct the AUTH string
AUTH = f'{BRIGHT_DATA_USERNAME}:{BRIGHT_DATA_PASSWORD}'
SBR_WS_CDP = f'wss://{AUTH}@brd.superproxy.io:9222'

# Ensure the output directory exists
output_dir = '/Users/tis/foam/github/PRH-API-Python-Client/external_repos/PrhScraper/test/out'
os.makedirs(output_dir, exist_ok=True)

async def run(pw):
    browser = await launch_browser(pw, headless=False)  # Ensure headless is set to False
    page = await browser.new_page()
    try:
        await navigate_to_page(page, 'https://virre.prh.fi')
        await search_company(page, '0217665-9')
        await wait_for_download_button(page)
        
        async with page.context.expect_page() as new_page_info:
            await page.click('button[name="_eventId_createElectronicTRExtract"]')
            print('Download PDF button clicked.')
        
        try:
            new_page = await new_page_info.value
            await new_page.wait_for_load_state()
            print('New page loaded.')
            
            # Get the URL of the PDF from the new page
            pdf_url = new_page.url
            print(f'PDF URL: {pdf_url}')
            
            # Get the cookies from the Playwright session
            cookies = await get_cookies(new_page)

            # Download the PDF using requests with the extracted cookies
            download_pdf_with_cookies(pdf_url, cookies, os.path.join(output_dir, 'downloaded_file.pdf'))
        
        except Exception as e:
            print(f'No new page opened: {e}')
            link_selector = 'a[href="/novus/reportdisplay"]'
            if await page.is_visible(link_selector):
                print('Link found on the same page. Clicking the link...')
                async with page.context.expect_page() as new_page_info:
                    await page.click(link_selector)
                    print('Link clicked.')
                
                new_page = await new_page_info.value
                await new_page.wait_for_load_state()
                print('New page loaded.')
                
                # Get the URL of the PDF from the new page
                pdf_url = new_page.url
                print(f'PDF URL: {pdf_url}')
                
                # Get the cookies from the Playwright session
                cookies = await get_cookies(new_page)

                # Download the PDF using requests with the extracted cookies
                download_pdf_with_cookies(pdf_url, cookies, os.path.join(output_dir, 'downloaded_file.pdf'))
        
        except Exception as e:
            print(f'An error occurred: {e}')
            if page:
                try:
                    await page.screenshot(path=os.path.join(output_dir, 'error.png'), full_page=True)
                    print('Screenshot saved as error.png')
                except Exception as screenshot_error:
                    print(f'Failed to take screenshot: {screenshot_error}')
        
        # Keep the browser open indefinitely for testing
        print("Browser will remain open for testing. Press Ctrl+C to exit.")
        await asyncio.Future()  # Run forever

    finally:
        await close_browser(browser)

def download_pdf_with_cookies(url, cookies, output_path):
    session = requests.Session()
    # Set the cookies in the requests session
    for name, value in cookies.items():
        session.cookies.set(name, value)

    response = session.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f'PDF downloaded and saved to {output_path}')


async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())