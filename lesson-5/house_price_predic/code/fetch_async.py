import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

links = list(pd.read_csv("ads.csv")["link"])[64:100]
print(links[:5])

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-web-security")
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-certificate-errors-spki-list")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins")
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

print("🚀 Chrome driver yaratilmoqda...")
try:
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)  # 20 soniya timeout
    driver.implicitly_wait(5)  # 5 soniya kutish
    wait = WebDriverWait(driver, 8)  # 8 soniya kutish
    data = []
    print("✅ Chrome driver tayyor!")
except Exception as e:
    print(f"❌ Chrome driver yaratishda xatolik: {e}")
    exit(1)

for i, url in enumerate(links, 1):
    print(f"\n📄 {i}/{len(links)} - Sahifa yuklanmoqda: {url}")
    
    # 3 marta urinish
    success = False
    for attempt in range(3):
        try:
            if attempt > 0:
                print(f"🔄 {attempt + 1}-urinish...")
                time.sleep(5)  # Har urinish orasida kutish
            
            driver.get(url)
            print("⏳ Sahifa yuklandi, elementlarni kutmoqda...")
            time.sleep(3)
            success = True
            break
            
        except TimeoutException:
            print(f"⏰ Timeout ({attempt + 1}/3): {url}")
            if attempt == 2:
                print(f"❌ 3 marta urinib ko'rdik, o'tkazib yuboramiz: {url}")
        except Exception as e:
            print(f"❌ Sahifa yuklashda xatolik ({attempt + 1}/3): {e}")
            if attempt == 2:
                print(f"❌ 3 marta urinib ko'rdik, o'tkazib yuboramiz: {url}")
    
    if not success:
        continue

    try:
        print("🔍 Narx elementini qidirmoqda...")
        price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="css-e2ir3r"]'))).text.strip()
        print(f"💰 Narx topildi: {price}")
        
        print("🔍 Viloyat va tuman ma'lumotlarini qidirmoqda...")
        state = driver.find_element(By.CSS_SELECTOR, 'div.css-1deibjd > p.css-7wnksb').text.strip()
        district = driver.find_element(By.CSS_SELECTOR, 'div.css-1deibjd > p.css-z0m36u').text.strip()
        print(f"📍 Joylashuv: {state}, {district}")
        print("🔍 Parametrlar konteynerini qidirmoqda...")
        container = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="ad-parameters-container"]')
        paragraphs = container.find_elements(By.TAG_NAME, 'p')
        info = {}
        print(f"📋 {len(paragraphs)} ta parametr topildi")

        for p in paragraphs:
            text = p.text.strip()
            if not text or ':' not in text:
                continue

            key, value = text.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            info[key] = value

        # Detect if the URL is in Uzbek (contains '/oz' after 'https://www.olx.uz/d/')
        uzbek_mode = False
        try:
            uzbek_mode = '/oz' in url.split('https://www.olx.uz/d/')[1].split('/')[0:2]
        except Exception:
            uzbek_mode = False
        
        if uzbek_mode:
            row = {
                "Price": price,
                "State": state,
                "District": district,
                "Rooms": info.get("xonalar soni", ""),
                "Total Area": info.get("umumiy maydon", ""),
                "Living Area": info.get("yashash maydoni", ""),
                "Location": info.get("joylashuvi", ""),
                "Floors": info.get("uy qavatliligi", ""),
                "Ceiling height": info.get("shifining balandligi", ""),
                "Furniture": info.get("mebelli", ""),
                "Land area": info.get("uchastka maydoni", ""),
                "Condition": info.get("uy holati", ""),
                "House type": info.get("uy turi", ""),
                "Building type": info.get("qurilish turi", ""),
                "Water": info.get("suv", ""),
                "Electricity": info.get("elektr ta'minoti", ""),
                "Heating": info.get("isitish", ""),
                "Gas": info.get("gaz", ""),
                "Year": info.get("uy qurilgan/topsirilgan yili", "")
            }
        else:
            row = {
                "Price": price,
                "State":state,
                "District":district,
                "Rooms": info.get("количество комнат", ""),
                "Total Area": info.get("общая площадь", ""),
                "Living Area": info.get("жилая площадь", ""),
                "Location": info.get("расположение", ""),
                "Floors": info.get("этажность дома", ""),
                "Ceiling height": info.get("высота потолков", ""),
                "Furniture": info.get("меблирована", ""),
                "Land area": info.get("площадь участка", ""),
                "Condition": info.get("состояние дома", ""),
                "House type": info.get("тип дома", ""),
                "Building type": info.get("тип строения", ""),
                "Water": info.get("вода", ""),
                "Electricity": info.get("электричество", ""),
                "Heating": info.get("отопление", ""),
                "Gas": info.get("газ", ""),
                "Year": info.get("год постройки/сдачи", "")
            }

        data.append(row)
        print(f"✅ Ma'lumot saqlandi! Jami: {len(data)} ta")
    
    except TimeoutException:
        print(f"⏰ Timeout xatoligi: {url}")
    except NoSuchElementException as e:
        print(f"🔍 Element topilmadi: {e} | Link: {url}")
    except Exception as e:
        print(f"❌ Umumiy xatolik: {e} | Link: {url}")

driver.quit()

if data:
    # Clean the data - remove newlines from all string fields
    for item in data:
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = ' '.join(value.split())
    
    df = pd.DataFrame(data)
    
    try:
        # Agar output.csv fayl mavjud bo'lsa, append qilish
        if os.path.exists("output.csv"):
            print("📁 Mavjud output.csv faylga qo'shilmoqda...")
            try:
                # Try reading with error handling for malformed CSV
                existing_df = pd.read_csv("output.csv", encoding='utf-8-sig', on_bad_lines='warn')
                
                # If the file is empty or corrupt, create a new DataFrame
                if existing_df.empty or len(existing_df.columns) == 0:
                    raise pd.errors.EmptyDataError
                    
                # Yangi ma'lumotlarni qo'shish
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                # Remove any potential duplicates
                combined_df = combined_df.drop_duplicates()
                combined_df.to_csv("output.csv", index=False, encoding='utf-8-sig', quoting=1)
                print(f"✅ {len(df)} ta yangi yozuv qo'shildi. Jami: {len(combined_df)} ta yozuv")
            except (pd.errors.ParserError, pd.errors.EmptyDataError):
                # If the file is corrupted, create a backup and start fresh
                print("⚠️ CSV faylda xatolik topildi. Yangi fayl yaratilmoqda...")
                os.rename("output.csv", f"output_backup_{int(time.time())}.csv")
                df.to_csv("output.csv", index=False, encoding='utf-8-sig', quoting=1)
                print(f"✅ Yangi output.csv fayl yaratildi: {len(df)} ta yozuv")
        else:
            print("📝 Yangi output.csv fayl yaratilmoqda...")
            df.to_csv("output.csv", index=False, encoding='utf-8-sig', quoting=1)
            print(f"✅ CSV fayl yaratildi: output.csv ({len(df)} ta yozuv)")
    except Exception as e:
        print(f"❌ CSV fayl bilan ishlashda xatolik: {e}")
else:
    print("⚠️ Hech qanday ma'lumot olinmadi!")
