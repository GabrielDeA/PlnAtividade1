import requests
from bs4 import BeautifulSoup

import json

def leituraClasse(classe):

    print(f'lendo o {classe}')

    # URL da página a ser raspada
    url = f"http://dnd5e.wikidot.com/{classe}"

    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    content = response.content

    # Cria o objeto BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Extrai todas as tags de títulos e parágrafos
    elementos = soup.find_all(['h1', 'h2', 'h3', 'ul', 'li', 'p', 'table'])
    h1uns = soup.find_all(['h1'])
    startElement = soup.find(class_='wiki-content-table')

    stopElement = soup.find(id="toc1")

    escrever = False

    textoUtil = []
    textoInutil = []
    arrayH3 = []
    livrosAEvitar = ["amonkhet", "unearthed arcana"]
    list_stack = []

    for elemento in elementos:
        if elemento == startElement:
            escrever = True

        if escrever:

            if elemento.name == 'h3':
                textoUtil.append(arrayH3)
                arrayH3 = []
                h3 = True

            if elemento.name == 'ul':
                new_list = []

                # Check if this <ul> is a child of the current list's <li>
                is_nested = False
                if list_stack and (elemento.parent.name == 'li') and elemento.parent in list_stack[-1]:
                    is_nested = True

                if is_nested:
                    list_stack[-1].append(new_list)
                    list_stack.append(new_list)
                else:
                    # It's a top-level list or a sibling list.
                    # Pop from the stack until it's empty to represent moving back to a top level.
                    while list_stack:
                        list_stack.pop()

                    #textoUtil.append(new_list)
                    arrayH3.append(new_list)
                    list_stack.append(new_list)
                continue

            # Check for the beginning of a list

            # Check if the current element is a li
            if elemento.name == 'li':
                # Only add if we're in a list and the element is a direct child of a ul.
                if list_stack and elemento.parent.name == 'ul':
                    list_stack[-1].append(elemento.text.strip())
                continue

            if elemento.name == 'table':
                tabela = []
                for tr in elemento.find_all('tr'):
                    arrayTh = []
                    #Não queremos conteúdos do Unearthed Arcana (UA)
                    #UA é um tipo de Beta test e seus conteúdos não foram oficializados
                    if any(palavra in tr.text.lower() for palavra in livrosAEvitar):
                        break

                    for th in tr.find_all('th'):
                        arrayTh.append(th.text)
                    if len(arrayTh) > 0:
                        tabela.append(arrayTh)

                    arrayTd = []
                    for td in tr.find_all('td'):
                        arrayTd.append(td.text)
                    if len(arrayTd) > 0:
                        tabela.append(arrayTd)

                textoUtil.append(tabela)
                continue

            # For non-list elements, we assume we've exited any list structure.
            while list_stack:
                list_stack.pop()

            #textoUtil.append(elemento.text.strip())
            arrayH3.append(elemento.text.strip())

    texto = [
        textoUtil,
        textoInutil,
    ]

    with open(f"JsonSoup/JsonClasses/{classe}.json", "w") as f:
        json.dump(texto, f, indent=4)

#leituraClasse("warlock")