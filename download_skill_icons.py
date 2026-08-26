#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# Create folder
os.makedirs("skill_icons", exist_ok=True)

# Get the page
url = "https://lootandwaifus.com/sword-x-staff-skill-database/"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')

# Find all card-icon images
images = soup.find_all('img', class_='card-icon')
print(f"Found {len(images)} images")

# Download each one
for img in images:
    src = img.get('src') or img.get('data-src')
    if src:
        # Get the skill name from alt attribute
        skill_name = img.get('alt', '')
        
        # Get extension from original file
        ext = os.path.splitext(src)[1] or '.png'
        
        if skill_name:
            # Keep the skill name as-is (keep apostrophes, spaces, etc.)
            # Just remove characters that are invalid for filenames on Mac
            # Invalid: / \ : * ? " < > |
            invalid_chars = '/\\:*?"<>|'
            for char in invalid_chars:
                skill_name = skill_name.replace(char, '')
            
            filename = f"{skill_name}{ext}"
        else:
            # Fallback to original filename if no alt text
            filename = os.path.basename(src)
        
        full_url = urljoin(url, src)
        filepath = os.path.join("skill_icons", filename)
        
        print(f"Downloading: {skill_name or filename}")
        img_data = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with open(filepath, 'wb') as f:
            f.write(img_data.content)
        print(f"  Saved: {filename}")

print(f"\n✅ Done! Downloaded to 'skill_icons' folder")
