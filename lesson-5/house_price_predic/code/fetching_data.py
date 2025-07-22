from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--user-agent=Mozilla/50 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

service = Service()
driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

base_url = "https://www.olx.uz/oz/nedvizhimost/doma/prodazha/tashkent/"
params = "?currency=UZS&search%5Bfilter_enum_private_house_type%5D%5B0%5D=1&search%5Bfilter_enum_private_house_type%5D%5B1%5D=3&search%5Bfilter_enum_private_house_type%5D%5B2%5D=2&search%5Bfilter_enum_private_house_type%5D%5B3%5D=5&search%5Bfilter_enum_private_house_type%5D%5B4%5D=6&search%5Bfilter_enum_location%5D%5B0%5D=1"

page = 1
all_ads = []

while True:
    url = f"{base_url}?page={page}&{params[1:]}"
    print(f"✅ Sahifa {page} yuklanyapti: {url}")
    driver.get(url)
    time.sleep(3)

    ads = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="listing-grid"] > div[data-cy="l-card"]')
    if not ads:
        print("❌ E’lon topilmadi. Tugadi.")
        break

    print(f"🔹 Sahifa {page} — {len(ads)} ta e’lon topildi.")
    
    for ad in ads:
        try:
            title_elem = ad.find_element(By.CSS_SELECTOR, 'h4')
            link_elem = ad.find_element(By.CSS_SELECTOR, 'a')

            ad_data = {
                "title": title_elem.text,
                "link": link_elem.get_attribute('href'),
            }
            all_ads.append(ad_data)
        except:
            continue
    if all_ads:
        for ad in all_ads[:5]:
            print(ad)
    else:
        print("❌ E’lon topilmadi. Tugadi.")

    if page == 25:
        break

    page += 1
    time.sleep(2)

driver.quit()

print(f"\n🔍 Umumiy yig‘ilgan e’lonlar soni: {len(all_ads)}")

with open('ads.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'link'])
    for ad in all_ads:
        writer.writerow([ad['title'], ad['link']])

for ad in all_ads[:5]:
    print(ad)
