

### Updated `pw_download.py`

import os
import asyncio
from playwright.async_api import Page

async def simulate_cmd_s(page: Page):
    try:
        if os.name == 'posix':  # macOS
            await page.keyboard.down('Meta')
        else:  # Windows/Linux
            await page.keyboard.down('Control')
        await page.keyboard.press('s')
        await page.keyboard.up('Meta' if os.name == 'posix' else 'Control')
        print('Simulated Cmd+S or Ctrl+S.')
        return True
    except Exception as e:
        print(f'Failed to simulate Cmd+S or Ctrl+S: {e}')
        return False

async def simulate_print(page: Page):
    try:
        await page.keyboard.down('Control')
        await page.keyboard.press('p')
        await page.keyboard.up('Control')
        print('Simulated Ctrl+P for print dialog.')
        return True
    except Exception as e:
        print(f'Failed to simulate Ctrl+P: {e}')
        return False

async def simulate_context_menu(page: Page):
    try:
        await page.mouse.click(100, 200, button='right')  # Adjust coordinates as needed
        print('Simulated right-click for context menu.')
        return True
    except Exception as e:
        print(f'Failed to simulate right-click: {e}')
        return False

async def trigger_download_via_js(page: Page, pdf_url: str):
    try:
        await page.evaluate(f'''
            const link = document.createElement('a');
            link.href = '{pdf_url}';
            link.download = 'downloaded_file.pdf';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        ''')
        print('Triggered download via JavaScript.')
        return True
    except Exception as e:
        print(f'Failed to trigger download via JavaScript: {e}')
        return False

async def wait_for_pdf_download(page: Page, output_dir: str):
    # Wait for the download event
    try:
        download = await page.wait_for_event('download')
        download_path = os.path.join(output_dir, download.suggested_filename)
        await download.save_as(download_path)
        print(f'PDF downloaded and saved as {download_path}')
    except Exception as e:
        print(f'Failed to download PDF: {e}')

async def download_pdf(page: Page, output_dir: str):
    try:
        # Try simulating Cmd+S or Ctrl+S
        if await simulate_cmd_s(page):
            print('Simulated Cmd+S or Ctrl+S successfully.')
            await wait_for_pdf_download(page, output_dir)
            return True
        else:
            print('Failed to simulate Cmd+S or Ctrl+S.')
            
            # Try simulating Ctrl+P for print dialog
            if await simulate_print(page):
                print('Simulated Ctrl+P successfully.')
                await wait_for_pdf_download(page, output_dir)
                return True
            else:
                print('Failed to simulate Ctrl+P.')
                
                # Try simulating right-click for context menu
                if await simulate_context_menu(page):
                    print('Simulated right-click successfully.')
                    await wait_for_pdf_download(page, output_dir)
                    return True
                else:
                    print('Failed to simulate right-click.')
                    
                    # Try triggering download via JavaScript
                    pdf_url = 'URL_OF_THE_PDF'  # Replace with the actual URL
                    if await trigger_download_via_js(page, pdf_url):
                        print('Triggered download via JavaScript successfully.')
                        await wait_for_pdf_download(page, output_dir)
                        return True
                    else:
                        print('Failed to trigger download via JavaScript.')
        return False
    except Exception as e:
        print(f'An error occurred while trying to download the PDF: {e}')
        return False

async def get_cookies(page: Page):
    cookies = await page.context.cookies()
    return {cookie['name']: cookie['value'] for cookie in cookies}