import pandas as pd
import re
import os

# Load CSV
df = pd.read_csv('../data/domuz_listings.csv')

# --- Clean square ---
df['square'] = df['square'].astype(str).str.replace('m²', '').str.strip().str.replace(',', '.')
df['square'] = pd.to_numeric(df['square'], errors='coerce')

# Filter square: > 15 and < 1400
df = df[(df['square'] > 15) & (df['square'] < 1400)]

# --- Clean price ---
df['price'] = df['price'].astype(str).str.replace(r'\D+', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Filter price: > 100 million
df = df[df['price'] > 100_000_000]

# --- Clean address ---
def extract_address(text):
    if isinstance(text, str) and text.startswith("Toshkent"):
        match = re.search(r'Toshkent,?\s*(.*?)\s*tumani', text)
        if match:
            return match.group(1).strip()
    return None

df['address'] = df['address'].apply(extract_address)

# Filter non-null addresss
df = df[df['address'].notnull()]

# --- Final Cleaned Data ---
clean_df = df[['square', 'price', 'address']]
# Append or create data
file_path = '../data/cleaned_data.csv'
new_data = pd.DataFrame(clean_df)

if os.path.exists(file_path):
    old_data = pd.read_csv(file_path)

    # Combine and remove duplicates (based on square + price + address)
    combined = pd.concat([old_data, new_data], ignore_index=True)
    combined = combined.drop_duplicates(subset=["square", "price", "address"])

    # Save back to the same file
    combined.to_csv(file_path, index=False, encoding='utf-8-sig')
else:
    new_data.to_csv(file_path, index=False, encoding='utf-8-sig')
print(clean_df)
