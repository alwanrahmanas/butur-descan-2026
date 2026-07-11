from selenium import webdriver
import time
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8091/')
time.sleep(3)
script = """
return {
  len: dataKeluarga.length,
  first_desa: dataKeluarga.length > 0 ? dataKeluarga[0].desa_kelurahan : 'none',
  target: lokusList[0],
  keys: dataKeluarga.length > 0 ? Object.keys(dataKeluarga[0]).join(', ') : 'none'
};
"""
print("EVAL:", driver.execute_script(script))
driver.quit()
