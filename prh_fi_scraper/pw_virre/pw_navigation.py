async def navigate_to_page(page, url):
    print(f'Navigating to {url}...')
    await page.goto(url, timeout=2*60*1000)
    print(f'Page navigated to {url}')

async def search_company(page, company_id):
    await page.fill('#criteriaText', company_id)
    print(f'Company ID {company_id} inserted into search box.')
    await page.click('button[name="_eventId_search"]')
    print('Search button clicked.')

async def wait_for_download_button(page):
    await page.wait_for_selector('button[name="_eventId_createElectronicTRExtract"]', timeout=2*60*1000)
    print('Download button is available.')