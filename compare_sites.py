import re

for village in ['Laangke', 'Lakonea', 'Malalanda']:
    with open(f'{village}/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'const lokusList = (.+?);', content)
    lokus = m.group(1) if m else 'NOT FOUND'
    m2 = re.search(r'SPREADSHEET_ID = "(.+?)"', content)
    ssid = m2.group(1) if m2 else 'NOT FOUND'
    m3 = re.search(r'GID_KELUARGA = "(.+?)"', content)
    gk = m3.group(1) if m3 else 'NOT FOUND'
    m4 = re.search(r'GID_INDIVIDU = "(.+?)"', content)
    gi = m4.group(1) if m4 else 'NOT FOUND'
    sheets = re.findall(r"parseXlsxSheet\(workbook, '(.+?)'\)", content)
    m5 = re.search(r'USE_LOCAL_XLSX = (.+?);', content)
    local = m5.group(1) if m5 else 'NOT FOUND'
    m6 = re.search(r'LOCAL_XLSX_PATH = (.+?);', content)
    path = m6.group(1) if m6 else 'NOT FOUND'
    m7 = re.search(r'<h1>Desa Cantik<br>(.*?)</h1>', content)
    title = m7.group(1) if m7 else 'NOT FOUND'
    
    print(f'=== {village} ===')
    print(f'  lokusList: {lokus}')
    print(f'  SPREADSHEET_ID: {ssid}')
    print(f'  GID_KELUARGA: {gk}')
    print(f'  GID_INDIVIDU: {gi}')
    print(f'  USE_LOCAL_XLSX: {local}')
    print(f'  LOCAL_XLSX_PATH: {path}')
    print(f'  Sheets parsed: {sheets}')
    print(f'  Hero title: {title}')
    print(f'  Total lines: {content.count(chr(10))}')
    print()
