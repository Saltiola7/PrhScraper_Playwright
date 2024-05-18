from playwright.async_api import Playwright, Browser

async def launch_browser(playwright: Playwright, headless: bool = True) -> Browser:
    browser = await playwright.chromium.launch(headless=headless)
    print("Browser launched!")
    return browser

async def close_browser(browser: Browser):
    await browser.close()
    print("Browser closed.")