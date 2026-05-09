import requests
import json

url = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

response = requests.get(url)

print(response.status_code)

# Raw text
raw_text = response.text

# Remove problematic control characters
clean_text = raw_text.replace("\r", "").replace("\t", " ")

# Parse JSON manually
data = json.loads(clean_text, strict=False)

print(type(data))
print(len(data))

# Save locally
with open("data/shl_catalog.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Catalog saved successfully")