import requests
from bs4 import BeautifulSoup

import json

def leituraRaca(raca):

    # URL da página a ser raspada
    url = f"http://dnd5e.wikidot.com/lineage:{raca}"

    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    content = response.content

    # Cria o objeto BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Extrai todas as tags de títulos e parágrafos
    titles = soup.find_all(['h1', 'h2', 'ul', 'p'])
    h1uns = soup.find_all(['h1'])
    startElement = soup.find(id="toc0")

    stopElement = soup.find(id="toc1")
    if h1uns.index(startElement) != len(h1uns):
        stopElement = h1uns[h1uns.index(startElement) + 1]

    escrever = False
    encontrouOutroLivro = False
    print()
    print('Stop: ', stopElement)
    print('Start: ', startElement)

    textoUtilDwarf = []
    textoInutilDwarf = []
    # Exibe os resultados
    for title in titles:
        if title == stopElement:
            print('parar!')
            escrever = False
            encontrouOutroLivro = True

        if title == startElement:
            print('escrever!')
            escrever = True
        if escrever:
            textoUtilDwarf.append(title.get_text()) ##.replace('\n', ''))
            print(title)
        if encontrouOutroLivro:
            textoInutilDwarf.append(title.get_text()) ##.replace('\n', ''))

    print('-------------- imprimindo h1uns ------------')
    for h1 in h1uns:
        print(h1.get_text())

    texto = [
        textoUtilDwarf,
        textoInutilDwarf,
    ]

    with open(f"texto{raca}.json", "w") as f:
        json.dump(texto, f, indent=4)
    print('-------------- imprimindo texto.json ------------')


leituraRaca("halfling")