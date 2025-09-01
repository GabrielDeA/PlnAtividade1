from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()
driver.get("https://dnd5e.wikidot.com/#toc2")

try:
    ListaRacaComum = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/div/div/div/div/div[4]/div[2]/div[4]/div/div[2]/div/div/div[1]/ul/li/ul')
    ItensListaRacaComum = ListaRacaComum.find_elements(By.TAG_NAME, 'li')

    #Separa o texto de cada ul em uma lista de strings
    ListaNomeRacas = []
    for item in ItensListaRacaComum:
        try:
            #cria pasta para cada raca da lista de racas
            os.mkdir(f'c:/RacasPLN/{item.text}')
        except Exception:
            print("Pastas ja criadas")
        ListaNomeRacas.append(item.text)

    for item in ListaNomeRacas:
        caminhoPaginaRaca = f"https://dnd5e.wikidot.com/lineage:{item}"
        nomeRaca = item

        driver.get(caminhoPaginaRaca)
        print(f"Raca: {nomeRaca}")

        time.sleep(10)

        #Captura a descricao da raca, tem uma mudança repentina no caminho XPath, caso falhe muda o XPath
        try:
            descricao = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/div/div/div/div/div[4]/p[1]/strong/em').text
            print(f"Descricao: {descricao}")
        except Exception as e:
            descricao = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/div/div/div/div/div[4]/p[1]/em/strong').text
            print(f"Descricao: {descricao}")
        
        #Popula cada arquivo txt de cada raca         
        with open(f"c:/RacasPLN/{item}/Player Handbook.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Descricao: {descricao}\n")


except Exception as e:
    print(e)
finally:
    driver.quit()