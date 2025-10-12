from playwright.sync_api import sync_playwright


def get_berlin_marathon_date():
    berlin_url = "https://www.bmw-berlin-marathon.com/en/registration/lottery"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(berlin_url)
        page.wait_for_selector("div.frame-inner p")

        date = page.inner_text("div.frame-inner p")
        text = page.inner_text("div.frame-inner p strong")

        
        date_text = text, date

        browser.close()
    
    return date_text


def main():
    date, text = get_berlin_marathon_date()
    print("Full date:", date)
    print("text:", text)
    
if __name__ == '__main__':
    main()