from playwright.sync_api import sync_playwright

def download_pdf():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://repositori.uji.es/xmlui/bitstream/handle/10234/49394/s74.pdf")

        # Wait for the PDF to load and potentially be embedded
        page.wait_for_load_state("networkidle")

        # Find the embedded PDF element
        pdf_element = page.query_selector('embed[type="application/pdf"]') 
        if pdf_element:
            #  Wait for the PDF to download.
            #  This will likely involve the browser opening a new window/tab for the download.
            #  It's a bit more complex, as we need to handle the new window.
            with page.expect_download() as download_info:
                download = download_info.value
                download.save_as("downloaded_s74.pdf")

                print("PDF downloaded successfully!")
        else:
            print("Unable to find embedded PDF element. Download failed.")

        browser.close()

if __name__ == "__main__":
    download_pdf()