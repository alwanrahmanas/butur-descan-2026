import re
import os

files = {
    'Lakonea': { 'id': '1DYL6xpUSEdrZrk6yFMaNFVz91MEVoMEA', 'name': 'Kelurahan Lakonea' },
    'Malalanda': { 'id': '1ciK-2G3mGooMNBLIPCCrQS1yniQoNbWg', 'name': 'Desa Malalanda' },
    'Laangke': { 'id': '1s0Z1q68cDCYUGecfKa1DXZbW7fKQQTAv', 'name': 'Desa Laangke' }
}

for folder, data in files.items():
    # Start from the fresh base copy
    filepath = os.path.join(folder, 'base.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update SPREADSHEET_ID
    content = content.replace(
        'const SPREADSHEET_ID = "1DYL6xpUSEdrZrk6yFMaNFVz91MEVoMEA";',
        f'const SPREADSHEET_ID = "{data["id"]}";'
    )
    
    # 2. Update lokusList
    content = content.replace(
        'const lokusList = ["Desa Malalanda", "Desa Laangke", "Kelurahan Lakonea"];',
        f'const lokusList = ["{data["name"]}"];'
    )
    
    # 3. Update Hero Title
    content = content.replace(
        '<h1>Desa Cantik Buton Utara</h1>',
        f'<h1>Desa Cantik<br>{data["name"]}</h1>'
    )
    
    # 4. Update Hero Description
    content = content.replace(
        'Prototype dashboard statistik berbasis <strong>Keluarga dan Individu</strong> untuk Desa Malalanda, Desa Laangke, dan Kelurahan Lakonea.',
        f'Prototype dashboard statistik berbasis <strong>Keluarga dan Individu</strong> khusus untuk wilayah <strong>{data["name"]}</strong>.'
    )
    
    # 5. Hide Filter with regex
    content = re.sub(
        r'<select id="filter-wilayah">.*?</select>',
        f'<select id="filter-wilayah" disabled style="background:var(--color-surface-2); cursor:not-allowed;"><option value="semua">{data["name"]}</option></select>',
        content,
        flags=re.DOTALL
    )
    
    # 6. Fix tabs in profil with regex
    content = re.sub(
        r'<div class="tabs" id="profilTabs">.*?</div>',
        f'<div class="tabs" id="profilTabs"><button class="tab-btn active" data-target="profil-{data["name"].lower().replace(" ", "-").replace(".", "")}">{data["name"]}</button></div>',
        content,
        flags=re.DOTALL
    )
    
    # 7. Remove raw data tables (HTML)
    content = re.sub(
        r'\s*<!-- Table -->\s*<div class="table-container">\s*<table id="tableKeluarga">.*?</table>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'\s*<!-- Table -->\s*<div class="table-container">\s*<table id="tableIndividu">.*?</table>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 8. Remove JS that populates tableKeluarga
    content = re.sub(
        r"\s*// Table\s*\n\s*const tbody = document\.querySelector\('#tableKeluarga tbody'\);.*?}\);",
        '',
        content,
        flags=re.DOTALL
    )
    
    # 9. Remove JS that populates tableIndividu
    content = re.sub(
        r"\s*// Table\s*\n\s*const tbody = document\.querySelector\('#tableIndividu tbody'\);.*?}\);",
        '',
        content,
        flags=re.DOTALL
    )

    # Write to index.html
    outpath = os.path.join(folder, 'index.html')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Remove temp base file
    os.remove(filepath)
    print(f'  {folder}/index.html - rebuilt successfully')

print('All done!')
