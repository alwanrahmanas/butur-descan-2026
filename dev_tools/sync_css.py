"""Sync CSS and font imports from Malalanda to Laangke and Lakonea."""
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Malalanda", "index.html")

with open(SRC, "r", encoding="utf-8") as f:
    src = f.read()

# Extract style block
style_match = re.search(r'(<style>.*?</style>)', src, re.DOTALL)
if not style_match:
    print("ERROR: Could not find <style> in Malalanda")
    exit(1)
new_style = style_match.group(1)
print(f"Extracted style block: {len(new_style)} chars")

# Extract font link
font_match = re.search(r'(<!-- Fonts -->.*?<!-- CDNs -->)', src, re.DOTALL)
if not font_match:
    print("ERROR: Could not find font block in Malalanda")
    exit(1)
new_fonts = font_match.group(1)
print(f"Extracted font block: {len(new_fonts)} chars")

for folder in ["Laangke", "Lakonea"]:
    target = os.path.join(BASE, folder, "index.html")
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace style block
    content = re.sub(r'<style>.*?</style>', new_style, content, count=1, flags=re.DOTALL)
    
    # Replace font block
    content = re.sub(r'<!-- Fonts -->.*?<!-- CDNs -->', new_fonts, content, count=1, flags=re.DOTALL)

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Updated: {folder}/index.html ({len(content)} chars)")

print("Done!")
