"""Update chart colors in Laangke and Lakonea to warm editorial palette."""
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Old colors -> New colors mapping
replacements = [
    # Chart text colors
    ("'#e1e6e3'", "'#e8e5df'"),
    ("'#193126'", "'#1a1a18'"),
    
    # isDark grid colors  
    ("'#2a3a30'", "'#333230'"),
    ("'#e8ede9'", "'#e8e3dc'"),
    
    # Chart palettes
    ("'#176a4d'", "'#8c5a3c'"),
    ("'#1f8fc8'", "'#5a7d6a'"),
    ("'#c7781f'", "'#c49a6c'"),
    ("'#cc3a3a'", "'#b85c4d'"),
    ("'#94a39b'", "'#a39080'"),
    ("'#6c5ce7'", "'#6b6860'"),
    ("'#fd79a8'", "'#d4a27a'"),
    ("'#1e9e57'", "'#5a7d6a'"),
    
    # Add borderRadius to bar charts  
    ("backgroundColor: '#176a4d'", "backgroundColor: '#8c5a3c', borderRadius: 3"),
    ("backgroundColor: '#1f8fc8' }", "backgroundColor: '#5a7d6a', borderRadius: 3 }"),
    ("backgroundColor: '#cc3a3a'", "backgroundColor: '#b85c4d', borderRadius: 3"),
    
    # Update chart legend font
    ("labels: { color: txtColor } }", "labels: { color: txtColor, font: { family: \"'Plus Jakarta Sans'\" } } }"),
]

for folder in ["Laangke", "Lakonea"]:
    target = os.path.join(BASE, folder, "index.html")
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    for old, new in replacements:
        content = content.replace(old, new)

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Updated chart colors: {folder}/index.html")

print("Done!")
