# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Firefox()
driver.get("https://dnd5e.wikidot.com/#toc2")

try:
    ListaRacaComum = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/div/div/div/div/div[4]/div[2]/div[4]/div/div[2]/div/div/div[1]/ul/li/ul')
    ItensListaRacaComum = ListaRacaComum.find_elements(By.TAG_NAME, 'li')

    ListaNomeRacas = []
    for item in ItensListaRacaComum:
        ListaNomeRacas.append(item.text)

    for item in ListaNomeRacas:
        caminhoPaginaRaca = f"https://dnd5e.wikidot.com/lineage:{item}"
        nomeRaca = item

        driver.get(caminhoPaginaRaca)
        print(f"Raca: {nomeRaca}")

        time.sleep(10)

        try:
            descricao = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/div/div/div/div/div[4]/p[1]/strong/em').text
            print(f"Descricao: {descricao}")
        except Exception as e:
            descricao = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/div/div/div/div/div[4]/p[1]/em/strong').text
            print(f"Descricao: {descricao}")
except Exception as e:
    print(e)
finally:
    driver.quit()